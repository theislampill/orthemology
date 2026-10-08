def operational_expand_value(value, mappings):
    if isinstance(value, str):
        def expand(match):
            require(match.group(1) in mappings, 'Missing source-owned operational mapping')
            return str(mappings[match.group(1)])
        return re.sub(r'\{((?:out|adapter|tool:[^{}]+|archive:[^{}]+|dependency:[^{}]+|input:[^{}]+|driver:[^{}]+))\}', expand, value)
    if isinstance(value, list):
        return [operational_expand_value(row, mappings) for row in value]
    if isinstance(value, dict):
        return {operational_expand_value(key, mappings): operational_expand_value(row, mappings) for key, row in value.items()}
    return value


def operational_symbolize(value, mappings):
    """Public evidence receives only adapter-owned tokens, never private paths."""
    if isinstance(value, str):
        for key, path in sorted(mappings.items(), key=lambda row: len(str(row[1])), reverse=True):
            value = value.replace(str(path), '{' + key + '}')
        return value
    if isinstance(value, list): return [operational_symbolize(row, mappings) for row in value]
    if isinstance(value, dict): return {operational_symbolize(key, mappings): operational_symbolize(row, mappings) for key, row in value.items()}
    return value


def operational_verify_tree(root, expected):
    root = no_symlinks(root).resolve(); actual = {}; directories = set()
    allowed = {p.as_posix() for name in expected for p in PurePosixPath(name).parents if str(p) != '.'}
    for path in root.rglob('*'):
        no_symlinks(path)
        if path.is_file():
            raw = path.read_bytes(); actual[path.relative_to(root).as_posix()] = {'sha256': sha(raw), 'bytes': len(raw)}
        else:
            require(path.is_dir(), 'Nonregular operational archive entry')
            directories.add(path.relative_to(root).as_posix())
    require(actual == expected and directories <= allowed, 'Original operational archive inventory changed')


def operational_verify_root(packet, root):
    owner = _OPERATIONAL_DATA['direct'].get(packet, _OPERATIONAL_DATA['popen'].get(packet))
    operational_verify_tree(root, owner['input_files'])


def operational_runpy(driver, arguments):
    old_argv, old_path = sys.argv, sys.path[:]
    try:
        sys.argv = [str(driver), *arguments]; sys.path[0] = str(driver.parent)
        try:
            runpy.run_path(str(driver), run_name='__main__')
        except SystemExit as end:
            require(end.code is None or type(end.code) is int and end.code == 0, 'Original driver exited unsuccessfully: ' + str(end.code))
    finally:
        sys.argv = old_argv; sys.path[:] = old_path


def operational_tracer_argv(stage, packet):
    return [stage['argv'][0], '-B', '{adapter}', '--trace-operational', packet,
            stage['argv'][2], '{out}/traces/' + stage['id'], *stage['argv'][3:]]


def operational_trace_context(packet, driver, trace, arguments):
    require(packet in _OPERATIONAL_DATA['packets'] and sys.flags.optimize == 0, 'Unapproved recipe or disabled original assertions')
    owner = _OPERATIONAL_DATA['packets'][packet]
    driver = no_symlinks(driver).resolve(); root = driver.parent
    require(sha(driver.read_bytes()) == owner['driver']['sha256'] and driver.name == PurePosixPath(owner['driver']['member_chain'][-1]).name,
            'Changed original operational driver')
    operational_verify_root(packet, root)
    require(Path.cwd().resolve() == root, 'Operational original must launch at exact archive root')
    suite = _OPERATIONAL_DATA['descriptors'][owner['suite_id']]
    original = next(s for s in suite['replay']['stages'] if s['kind'] == 'DRIVER')
    require(len(arguments) == len(original['argv']) - 3 and arguments[::2] == original['argv'][3::2], 'Changed operational original flags')
    args = dict(zip(arguments[::2], arguments[1::2]))
    require('--check-only' not in args, 'Check-only cannot qualify a complete recipe')
    lean = no_symlinks(args['--lean'] if '--lean' in args else str(Path(args['--lean-root']) / 'bin/lean')).resolve()
    require(sha(lean.read_bytes()) == LEAN_SHA, 'Operational compiler differs from pinned tool')
    # Match the established hash-checked interpreter-symlink exception while
    # retaining the original sys.executable spelling in nested source argv.
    python = Path(sys.executable).absolute()
    expected_python = next(t['executable_sha256'] for t in suite['replay']['tools'] if t['name'] == 'python')
    require(sha(python.read_bytes()) == expected_python, 'Operational Python differs from pinned tool')
    output = no_symlinks(args['--output']).absolute()
    require(output.name == 'original' and not output.exists() and output != root and not output.is_relative_to(root), 'Original output must be fresh and external')
    trace = no_symlinks(trace).absolute()
    require(trace == output.parent / 'traces/original-driver' and not trace.exists(), 'Trace must be exact fresh adapter output')
    mathlib = no_symlinks(args.get('--mathlib', args.get('--mathlib-root'))).resolve()
    mappings = {'archive:source-archive': root, 'driver:original': driver, 'out': output.parent,
        'tool:lean': lean, 'tool:lean-root': lean.parent.parent, 'tool:python': python,
        'dependency:mathlib': mathlib, 'adapter': Path(__file__).resolve()}
    if packet == 't08-batch':
        source_zip = no_symlinks(args['--source-zip']).resolve()
        pin = _OPERATIONAL_DATA['popen'][packet]['source_archive_binding']
        require(source_zip.stat().st_size == pin['bytes'] and sha(source_zip.read_bytes()) == pin['sha256'], 'Nested original archive differs')
        mappings['input:batch-science-archive'] = source_zip
    require(arguments == [_expand(arg, mappings) for arg in original['argv'][3:]], 'Original source argument values changed')
    return driver, trace, mappings, operational_expand_value(_OPERATIONAL_DATA['execution_plans'][packet]['plan'], mappings)


def operational_trace(packet, driver, trace, arguments):
    driver, trace, mappings, p = operational_trace_context(packet, driver, trace, arguments)
    root = driver.parent; trace.mkdir(parents=True)
    old_run, old_popen = subprocess.run, subprocess.Popen
    try:
        if packet in _OPERATIONAL_DATA['direct']:
            calls = trace / 'calls'; calls.mkdir()
            hook = operational_direct_source_bound_run(old_run, calls, p)
            subprocess.run = hook
            operational_runpy(driver, arguments); hook.finish()
        elif packet == 't09-controller':
            with _operational_popen_PopenCapture(old_popen, trace / 'calls', p['children']) as hook:
                subprocess.Popen = hook
                operational_runpy(driver, arguments); hook.finish()
        else:
            review = trace / 'review'; review.mkdir()
            direct_hook = _operational_nested_bound_run(_operational_nested_run_without_outer_popen(old_run, old_popen), review, p['review_children'])
            nested = p['nested_parent']
            # The source-facing command is unchanged. Only its reviewed capture
            # transport is inserted, and both vectors enter the physical ledger.
            with _operational_popen_PopenCapture(old_popen, trace / 'nested', [nested]) as parent_hook:
                def guarded_nested(argv, *args, **kwargs):
                    operational_verify_tree(Path(p['nested_source_root']), _OPERATIONAL_DATA['popen'][packet]['source_input_files'])
                    return parent_hook(argv, *args, **kwargs)
                subprocess.run = direct_hook; subprocess.Popen = guarded_nested
                operational_runpy(driver, arguments)
                parent_hook.finish(); direct_hook.finish()
            operational_verify_tree(Path(p['nested_source_root']), _OPERATIONAL_DATA['popen'][packet]['source_input_files'])
        operational_verify_root(packet, root)
    finally:
        subprocess.run, subprocess.Popen = old_run, old_popen
    return 0


def operational_trace_batch_source(driver, trace, arguments):
    require(sys.flags.optimize == 0 and len(arguments) == 8 and arguments[::2] == ['--lean-root', '--mathlib', '--output', '--stage-timeout'] and arguments[-1] == '300.0',
            'Changed nested source arguments or disabled assertions')
    owner = _OPERATIONAL_DATA['popen']['t08-batch']
    driver = no_symlinks(driver).resolve(); root = driver.parent
    require(sha(driver.read_bytes()) == owner['source_driver']['sha256'], 'Nested source generator changed')
    operational_verify_tree(root, owner['source_input_files'])
    output = no_symlinks(arguments[5]).absolute(); original = output.parent
    require(output.name == 'fresh science' and not output.exists() and root == original / 'extracted source/Eighth_Actual_Batch_Controller_Source',
            'Nested original-owned source/output layout changed')
    trace = no_symlinks(trace).absolute()
    require(trace == original.parent / 'traces/original-driver/science' and not trace.exists(), 'Nested trace is not fresh')
    lean = no_symlinks(Path(arguments[1]) / 'bin/lean').resolve(); python = Path(sys.executable).absolute()
    require(sha(lean.read_bytes()) == LEAN_SHA and sha(python.read_bytes()) == 'd1483a82342508f2ec2b172b788d5b676a59eaf70ed01ae846a0f84f63a3a82a', 'Nested exact tool changed')
    mappings = {'archive:source-archive': Path.cwd().resolve(), 'out': original.parent, 'tool:lean': lean,
        'tool:lean-root': lean.parent.parent, 'tool:python': python, 'dependency:mathlib': no_symlinks(arguments[3]).resolve(), 'adapter': Path(__file__).resolve()}
    p = operational_expand_value(_OPERATIONAL_DATA['execution_plans']['t08-batch']['plan'], mappings)
    require(arguments == p['source_args'], 'Nested exact source argv changed')
    trace.mkdir(parents=True)
    old_run, old_popen = subprocess.run, subprocess.Popen
    hook = _operational_nested_bound_run(old_run, trace, p['science_children'])
    try:
        subprocess.run = hook
        operational_runpy(driver, arguments); hook.finish()
        operational_verify_tree(root, owner['source_input_files'])
    finally:
        subprocess.run, subprocess.Popen = old_run, old_popen
    return 0

OPERATIONAL_INFRA = re.compile(r'unknown module|unknown constant|unknown identifier|unknown namespace|no such file|file not found|failed to read file|object file|timed out|out of memory|maximum (?:recursion|heartbeats)|deterministic timeout', re.I)
OPERATIONAL_DRIVER_SHA = {key: value['driver']['sha256'] for key, value in _OPERATIONAL_DATA['packets'].items()}
OPERATIONAL_NONEXEC_SOURCE_SHA = 'ae0d5b1e2e0bb5c4bfb7a07c54aa77ea787d07ef3e60fb671751a6bb225a12c1'


