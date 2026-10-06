def operational_traced_run(original_run, trace, commands, *, metadata=None):
    """Capture only an exact reviewed serial list with original explicit cwd.

    Commands are constructed from adapter-owned source recipe constants and
    verified archive/output mappings, never from a producer receipt. This is
    the subprocess.run form shared by four reviewed D05/D07 source wrappers;
    Popen/nested companion forms are deliberately outside this contract.
    """
    require(isinstance(commands, list) and commands, 'Missing operational command contract')
    for row in commands:
        keys(row, {'argv', 'cwd', 'timeout'})
        require(isinstance(row['argv'], list) and row['argv'] and all((isinstance(v, str) and v and ('\x00' not in v) for v in row['argv'])), 'Malformed operational command')
        require(isinstance(row['cwd'], str) and Path(row['cwd']).is_absolute(), 'Operational command cwd must be explicit')
        require(type(row['timeout']) in {int, float} and math.isfinite(row['timeout']) and (0 < row['timeout'] <= 86400), 'Invalid operational child timeout')
    if metadata is not None:
        keys(metadata, {'argv', 'cwd', 'timeout', 'form'})
        require(metadata['form'] in {'SPLIT_VERSION', 'MERGED_VERSION'}, 'Unreviewed operational metadata form')
        require(isinstance(metadata['argv'], list) and metadata['argv'] and all((isinstance(v, str) and v for v in metadata['argv'])), 'Malformed operational metadata argv')
        require(isinstance(metadata['cwd'], str) and Path(metadata['cwd']).is_absolute(), 'Unbound metadata cwd')
        require(type(metadata['timeout']) in {int, float} and math.isfinite(metadata['timeout']) and (0 < metadata['timeout'] <= 30), 'Invalid metadata budget')
    capture = traced_run(original_run, trace)
    position = 0
    metadata_done = metadata is None

    def merged_form(kwargs, contract):
        require(set(kwargs) == {'env', 'cwd', 'text', 'stdout', 'stderr', 'timeout'} and isinstance(kwargs['env'], dict), 'Changed operational subprocess form')
        require(str(Path(kwargs['cwd']).absolute()) == contract['cwd'] and type(kwargs['timeout']) in {int, float} and (kwargs['timeout'] == contract['timeout']), 'Changed operational cwd or child budget')
        require(kwargs['text'] is True and kwargs['stdout'] == subprocess.PIPE and (kwargs['stderr'] == subprocess.STDOUT), 'Changed operational output capture')

    def capture_metadata(argv, kwargs):
        directory = path_in(trace, 'metadata')
        require(not directory.exists(), 'Metadata capture already exists')
        directory.mkdir()
        record = {'argv': argv, 'cwd': metadata['cwd'], 'started_at': utc(), 'ended_at': None, 'terminal': 'RUNNING', 'exit_code': None, 'stdout_sha256': None, 'stderr_sha256': None}
        write_json(directory / '0000.json', record)

        def save(stdout, stderr, code, terminal):
            stdout = stdout or b''
            stderr = stderr or b''
            if isinstance(stdout, str):
                stdout = stdout.encode('utf-8')
            if isinstance(stderr, str):
                stderr = stderr.encode('utf-8')
            (directory / '0000.stdout').write_bytes(stdout)
            (directory / '0000.stderr').write_bytes(stderr)
            record.update(ended_at=utc(), terminal=terminal, exit_code=code, stdout_sha256=sha(stdout), stderr_sha256=sha(stderr))
            write_json(directory / '0000.json', record)
        try:
            result = original_run(argv, **kwargs)
        except subprocess.CalledProcessError as error:
            completed = type(error.returncode) is int and 0 <= error.returncode < 124
            save(error.stdout, error.stderr, error.returncode if completed else None, 'COMPLETED' if completed else 'INTERRUPTED')
            raise
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            save(getattr(error, 'stdout', None), getattr(error, 'stderr', None), None, 'TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'INTERRUPTED')
            raise
        completed = type(result.returncode) is int and 0 <= result.returncode < 124
        save(result.stdout, result.stderr, result.returncode if completed else None, 'COMPLETED' if completed else 'INTERRUPTED')
        return result

    def invoke(argv, *args, **kwargs):
        nonlocal position, metadata_done
        if not metadata_done:
            require(not args and argv == metadata['argv'], 'Original metadata probe was omitted or changed')
            if metadata['form'] == 'SPLIT_VERSION':
                require(set(kwargs) == {'capture_output', 'text', 'check', 'timeout'} and kwargs['capture_output'] is True and (kwargs['text'] is True) and (kwargs['check'] is True) and (type(kwargs['timeout']) in {int, float}) and (kwargs['timeout'] == metadata['timeout']) and (str(Path.cwd()) == metadata['cwd']), 'Changed split-stream metadata subprocess form')
            else:
                merged_form(kwargs, metadata)
            metadata_done = True
            return capture_metadata(argv, kwargs)
        require(not args and position < len(commands) and (argv == commands[position]['argv']), 'Unreviewed or repeated operational physical command')
        contract = commands[position]
        merged_form(kwargs, contract)
        destination = None
        if '-o' in argv:
            destination = Path(argv[argv.index('-o') + 1])
            if not destination.is_absolute():
                destination = Path(contract['cwd']) / destination
            require(not no_symlinks(destination).exists(), 'Operational child output already exists')
        index = position
        position += 1
        try:
            return capture(argv, **kwargs)
        finally:
            record_path = path_in(trace, f'{index:04}.json')
            if record_path.is_file():
                row = read_json(record_path)
                hashes = {}
                if destination is not None and no_symlinks(destination).is_file():
                    hashes[str(destination)] = sha(destination.read_bytes())
                row['output_hashes'] = hashes
                write_json(record_path, row)

    def finish():
        require(metadata_done and position == len(commands), 'Original serial call census is incomplete')
    invoke.finish = finish
    return invoke

def operational_direct_contract(packet):
    require(packet in _OPERATIONAL_DATA["direct"], "Unreviewed direct-run operational family")
    return _OPERATIONAL_DATA["direct"][packet]
def operational_direct_verify_sources(packet, root):
    owner = operational_direct_contract(packet)
    root = _operational_api.no_symlinks(root).resolve()
    expected = owner['input_files']
    actual = {}
    for path in root.rglob('*'):
        _operational_api.no_symlinks(path)
        if path.is_file():
            body = path.read_bytes()
            actual[path.relative_to(root).as_posix()] = {'sha256': _operational_api.sha(body), 'bytes': len(body)}
        else:
            _operational_api.require(path.is_dir(), 'Nonregular original source input')
    _operational_api.require(actual == expected, 'Original source bytes or inventory changed')
    _operational_api.require(actual['replay.py']['sha256'] == owner['driver_sha256'], 'Original driver changed')
    return owner

def operational_direct_source_plan(packet, root, output, lean, launch_cwd):
    root = _operational_api.no_symlinks(root).resolve()
    output = _operational_api.no_symlinks(output).absolute()
    lean = _operational_api.no_symlinks(lean).absolute()
    launch_cwd = _operational_api.no_symlinks(launch_cwd).resolve()
    owner = operational_direct_verify_sources(packet, root)
    _operational_api.require(output != root and (not output.is_relative_to(root)), 'Output overlaps original sources')
    children = []
    for old in owner['children']:
        row = copy.deepcopy(old)
        probe = row['role'] == 'TOOL_IDENTITY'
        generated = row['role'] == 'GENERATED_AXIOM_AUDIT'
        row['binding_kind'] = 'TOOL_PROBE' if probe else 'GENERATED_BY_ORIGINAL' if generated else 'ORIGINAL_SOURCE'
        row['binding_owner_sha256'] = owner['driver_sha256'] if probe or generated else row['source_sha256']
        row['cwd'] = str(root)
        row['log_assembly'] = 'STDOUT_WITH_MERGED_STDERR'
        row['timeout'] = 180 if packet == 't09-transport' else 30 if probe else 300
        if probe:
            row['argv'] = [str(lean), '--version']
            row['tool_sha256'] = _operational_api.LEAN_SHA
        else:
            if generated:
                name = row['module'] + '.lean'
                spec = owner['generated_sources'][name]
                source = _operational_api.path_in(output, name)
                row['generated_source_sha256'] = spec['sha256']
                row['generated_text'] = spec['text']
            else:
                source = _operational_api.path_in(root, row['source_path'])
            argv = [str(lean), '-j1']
            if packet == 't08-common':
                argv += ['-s65536', '--root=' + str(source.parent)]
            if row['output_path']:
                argv += ['-o', str(_operational_api.path_in(output, row['output_path']))]
            row['argv'] = argv + [str(source)]
            row['actual_source_path'] = str(source)
        children.append(row)
    metadata = None
    if owner['metadata_probe']:
        metadata = {'argv': [str(lean), '--version'], 'cwd': str(launch_cwd if packet == 't08-common' else root), 'timeout': 30, 'form': owner['metadata_probe']}
    return {'packet': packet, 'owner': owner, 'children': children, 'metadata': metadata, 'physical_child_count': len(children) + int(metadata is not None), 'original_receipt_child_count': len(children), 'required_post_dependency_readback': owner['post_dependency_readback'], 'inherited_only_wrapper_checks': 23 if packet == 't08-controller' else 0}

def operational_direct_check_child(spec, original, captured, parent, raw, source_bytes, object_bytes):
    """Check one real captured child against the immutable source-owned plan.

    Returned classifications are private proposal data. They do not themselves
    admit a public evidence schema or establish a theorem/control disposition.
    """
    _operational_api.require(parent['terminal'] == 'COMPLETED' and type(parent['exit_code']) is int and (parent['exit_code'] == 0), 'Original parent did not complete')
    _operational_api.require(captured['terminal'] == 'COMPLETED' and type(captured['exit_code']) is int and (captured['exit_code'] == spec['expected_exit']), 'Child lacks expected actual completion')
    _operational_api.require(type(original['exit_code']) is int and original['exit_code'] == captured['exit_code'] and (original.get('timed_out', False) is False), 'Original child and physical terminal differ')
    _operational_api.require(original[spec['receipt_key']] == spec['receipt_name'], 'Wrong original receipt child')
    _operational_api.require(captured['argv'] == spec['argv'] and captured['cwd'] == spec['cwd'], 'Actual child argv or cwd changed')
    if 'command' in original:
        _operational_api.require(original['command'] == captured['argv'], 'Original recorded argv changed')
    if 'compiler_cwd' in original:
        _operational_api.require(original['compiler_cwd'] == captured['cwd'], 'Original recorded cwd changed')
    _operational_api.require(all((isinstance(captured[k], str) and captured[k].endswith('Z') for k in ('started_at', 'ended_at'))) and parent['started_at'] <= captured['started_at'] <= captured['ended_at'] <= parent['ended_at'], 'Child interval was not measured within parent')
    log_sha = _operational_api.sha(raw)
    _operational_api.require(captured['log_sha256'] == original['log_sha256'] == log_sha, 'Original/captured log bytes differ')
    text = raw.decode('utf-8')
    kind = spec['binding_kind']
    source_sha = None
    if kind == 'ORIGINAL_SOURCE':
        source_sha = _operational_api.sha(source_bytes)
        _operational_api.require(source_sha == spec['source_sha256'], 'Original child source changed')
    elif kind == 'GENERATED_BY_ORIGINAL':
        source_sha = _operational_api.sha(source_bytes)
        _operational_api.require(source_bytes == spec['generated_text'].encode() and source_sha == spec['generated_source_sha256'], 'Generated original audit source changed')
    else:
        _operational_api.require(kind == 'TOOL_PROBE' and source_bytes is None and (object_bytes is None) and (spec['tool_sha256'] == _operational_api.LEAN_SHA) and ('4.19.0' in text) and ('6caaee842e94' in text), 'Original tool identity probe differs')
    if 'source_sha256' in original:
        _operational_api.require(original['source_sha256'] == source_sha, 'Original child source association differs')
    if spec['expected_exit']:
        resource = 'maximum recursion depth|maximum number of heartbeats|out of memory|unknown module prefix|object file .* does not exist|file not found|cannot open|REPLAY_TIMEOUT|interrupted'
        _operational_api.require('error:' in text and (not re.search(resource, text, re.I)), 'Resource/infrastructure failure is not semantic rejection')
        for literal in spec['required_literals']:
            _operational_api.require(literal in text, 'Missing source-owned diagnostic literal')
        for pattern in spec['required_regexes']:
            _operational_api.require(re.search(pattern, text, re.S) is not None, 'Missing source-owned diagnostic pattern')
        _operational_api.require(spec['required_literals'] or spec['required_regexes'], 'Unbound negative diagnostic')
        if spec['classification']:
            _operational_api.require(original.get('classification') == spec['classification'], 'Original rejection classification changed')
        if 'required_diagnostics' in original:
            _operational_api.require(original['required_diagnostics'] == spec['required_regexes'], 'Original diagnostic contract changed')
    elif kind != 'TOOL_PROBE':
        if spec['id'] == 'ReviewerControls':
            _operational_api.require(source_sha == 'db9737455bc7109fd40e7ff10812604000d18d650bb4868f1007790db1c9ebe8' and type(original.get('accepted_exact_historical_lint_count')) is int and (original['accepted_exact_historical_lint_count'] == 2), 'Changed exact historical lint exception')
            note = 'note: this linter can be disabled with `set_option linter.unnecessarySimpa false`\n'
            allowed = [spec['actual_source_path'] + ":66:44: warning: try 'simp at quorum' instead of 'simpa using quorum'\n" + note, spec['actual_source_path'] + ":75:8: warning: try 'simp at certificate' instead of 'simpa using certificate'\n" + note]
            for message in allowed:
                _operational_api.require(text.count(message) == 1, 'Exact historical lint message missing or duplicated')
                text = text.replace(message, '', 1)
        _operational_api.require(not re.search('warning:|error:|sorryAx', text), 'Positive compiler diagnostic is not clean')
    outputs = {}
    if spec['output_path']:
        _operational_api.require(isinstance(object_bytes, bytes), 'Missing fresh child object')
        object_sha = _operational_api.sha(object_bytes)
        path = spec['argv'][spec['argv'].index('-o') + 1]
        outputs[path] = object_sha
        for field in ('olean_sha256', 'object_sha256'):
            if field in original:
                _operational_api.require(original[field] == object_sha, 'Original object digest differs')
    else:
        _operational_api.require(object_bytes is None, 'Check-only stage acquired object credit')
    _operational_api.require(captured.get('output_hashes') == outputs, 'Fresh object changed since physical producer exit')
    result = {'source_child_id': spec['id'], 'binding_kind': kind, 'binding_owner_sha256': spec['binding_owner_sha256'], 'terminal': captured['terminal'], 'exit_code': captured['exit_code'], 'actual_outcome': 'REJECT' if spec['expected_exit'] else 'ACCEPT', 'argv': captured['argv'], 'cwd': captured['cwd'], 'started_at': captured['started_at'], 'ended_at': captured['ended_at'], 'log_sha256': log_sha, 'log_assembly': spec['log_assembly'], 'output_hashes': outputs, 'original_record_sha256': _operational_api.canonical(original), 'theorem_credit': False}
    if kind == 'ORIGINAL_SOURCE':
        result['source_sha256'] = source_sha
    elif kind == 'GENERATED_BY_ORIGINAL':
        result['generated_source_sha256'] = source_sha
    else:
        result['tool_sha256'] = spec['tool_sha256']
    return result

def operational_direct_source_bound_run(original_run, trace, plan):
    """Use only with the adapter-owned result of source_plan, never receipt argv."""
    specs = plan['children']
    position = 0
    metadata_pending = plan['metadata'] is not None
    commands = [{key: row[key] for key in ('argv', 'cwd', 'timeout')} for row in specs]
    captured_run = _operational_api.operational_traced_run(original_run, trace, commands, metadata=plan['metadata'])

    def invoke(argv, *args, **kwargs):
        nonlocal position, metadata_pending
        if metadata_pending:
            result = captured_run(argv, *args, **kwargs)
            metadata_pending = False
            return result
        _operational_api.require(position < len(specs) and argv == specs[position]['argv'], 'Unreviewed original child order/argv')
        spec = specs[position]
        if spec['binding_kind'] == 'TOOL_PROBE':
            _operational_api.require(_operational_api.sha(_operational_api.no_symlinks(argv[0]).read_bytes()) == _operational_api.LEAN_SHA, 'Original tool changed before launch')
        else:
            source = _operational_api.no_symlinks(spec['actual_source_path']).read_bytes()
            if spec['binding_kind'] == 'GENERATED_BY_ORIGINAL':
                _operational_api.require(source == spec['generated_text'].encode() and _operational_api.sha(source) == spec['generated_source_sha256'], 'Generated source changed before actual compilation')
            else:
                _operational_api.require(spec['binding_kind'] == 'ORIGINAL_SOURCE' and _operational_api.sha(source) == spec['source_sha256'], 'Original source changed before actual compilation')
        position += 1
        return captured_run(argv, *args, **kwargs)

    def finish():
        _operational_api.require(not metadata_pending and position == len(specs), 'Source-bound original call census incomplete')
        captured_run.finish()
    invoke.finish = finish
    return invoke

def operational_direct_exact_axioms(text, expected_names):
    observed = {}
    for name, raw in re.findall("'([^']+)' depends on axioms:\\s*\\[([^]]*)\\]", text, re.S):
        axes = sorted({value.strip() for value in raw.split(',') if value.strip()})
        _operational_api.require(name not in observed and set(axes) <= _operational_api.AXIOMS, 'Duplicate or unapproved original axiom audit')
        observed[name] = axes
    for name in re.findall("'([^']+)' does not depend on any axioms", text):
        _operational_api.require(name not in observed, 'Duplicate original axiom audit')
        observed[name] = []
    _operational_api.require(len(expected_names) == len(set(expected_names)) and set(observed) == set(expected_names), 'Incomplete or changed original axiom target inventory')
    return observed

def operational_direct_check_metadata(plan, trace, parent, receipt, output, lean):
    spec = plan['metadata']
    directory = _operational_api.path_in(trace, 'metadata')
    _operational_api.require({p.name for p in directory.iterdir()} == {'0000.json', '0000.stdout', '0000.stderr'}, 'Original metadata capture census differs')
    row = _operational_api.read_json(directory / '0000.json')
    _operational_api.keys(row, {'argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'stdout_sha256', 'stderr_sha256'})
    _operational_api.require(row['argv'] == spec['argv'] and row['cwd'] == spec['cwd'] and (row['terminal'] == 'COMPLETED') and (type(row['exit_code']) is int) and (row['exit_code'] == 0), 'Original version probe did not complete as prescribed')
    _operational_api.require(parent['started_at'] <= row['started_at'] <= row['ended_at'] <= parent['ended_at'], 'Metadata interval is outside original parent')
    stdout = _operational_api.no_symlinks(directory / '0000.stdout').read_bytes()
    stderr = _operational_api.no_symlinks(directory / '0000.stderr').read_bytes()
    _operational_api.require(_operational_api.sha(stdout) == row['stdout_sha256'] and _operational_api.sha(stderr) == row['stderr_sha256'], 'Original metadata bytes changed')
    text = stdout.decode('utf-8')
    _operational_api.require('4.19.0' in text and '6caaee842e94' in text and (text.strip() == receipt['compiler_version']), 'Original compiler version differs')
    _operational_api.require(_operational_api.sha(_operational_api.no_symlinks(lean).read_bytes()) == _operational_api.LEAN_SHA, 'Original tool fingerprint changed')
    if plan['packet'] == 't08-controller':
        _operational_api.require((output / 'logs/version.log').read_bytes() == stdout and (not stderr), 'Original merged version log differs')
    return {**row, 'source_child_id': '_original_version_probe', 'binding_kind': 'TOOL_PROBE', 'binding_owner_sha256': plan['owner']['driver_sha256'], 'tool_sha256': _operational_api.LEAN_SHA, 'original_receipt_row': False, 'theorem_credit': False}

def operational_direct_collect_original(packet, root, output, trace, parent, parent_text, lean, launch_cwd):
    """Read the entire actual original ledger; never execute or qualify it.

    The public adapter still owns source/descriptor admission, post-dependency
    readback, public source associations, wrapper controls, and target closure.
    """
    root = _operational_api.no_symlinks(root).resolve()
    output = _operational_api.no_symlinks(output).resolve()
    trace = _operational_api.no_symlinks(trace).resolve()
    _operational_api.require(parent['terminal'] == 'COMPLETED' and type(parent['exit_code']) is int and (parent['exit_code'] == 0), 'Original driver did not complete')
    plan = operational_direct_source_plan(packet, root, output, lean, launch_cwd)
    owner = plan['owner']
    _operational_api.require(_operational_api.sha(_operational_api.no_symlinks(lean).read_bytes()) == _operational_api.LEAN_SHA, 'Original tool fingerprint changed')
    receipt_path = _operational_api.path_in(output, owner['receipt'])
    receipt = _operational_api.read_json(receipt_path)
    _operational_api.require(receipt['status'] == owner['status'], 'Original full driver lacks its terminal receipt')
    for key, value in owner['required_fields'].items():
        _operational_api.require(type(receipt.get(key)) is type(value) and receipt[key] == value, 'Original terminal field differs: ' + key)
    manifest = 'MANIFEST.json' if packet == 't09-transport' else 'PUBLIC_MANIFEST.json'
    manifest_field = 'source_manifest_sha256' if packet == 't09-transport' else 'public_manifest_sha256'
    _operational_api.require(receipt[manifest_field] == owner['input_files'][manifest]['sha256'], 'Original receipt source manifest differs')
    rows = receipt['stages']
    specs = plan['children']
    _operational_api.require(len(rows) == len(specs) and all((row[spec['receipt_key']] == spec['receipt_name'] for row, spec in zip(rows, specs))), 'Original receipt stage inventory/order differs')
    trace_names = {f'{index:04}.{suffix}' for index in range(len(specs)) for suffix in ('json', 'log')}
    if plan['metadata']:
        trace_names.add('metadata')
    _operational_api.require({p.name for p in trace.iterdir()} == trace_names, 'Missing or extra physical child capture')
    children = []
    objects = {}
    audits = {}
    for index, (spec, original) in enumerate(zip(specs, rows)):
        captured = _operational_api.read_json(_operational_api.path_in(trace, f'{index:04}.json'))
        _operational_api.keys(captured, {'index', 'argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'output_hashes'})
        _operational_api.require(type(captured['index']) is int and captured['index'] == index, 'Physical child order differs')
        raw = _operational_api.path_in(trace, f'{index:04}.log').read_bytes()
        _operational_api.require(raw == _operational_api.path_in(output, spec['log_path']).read_bytes(), 'Original output log differs from captured stream')
        source = None if spec['binding_kind'] == 'TOOL_PROBE' else _operational_api.no_symlinks(spec['actual_source_path']).read_bytes()
        obj = _operational_api.path_in(output, spec['output_path']).read_bytes() if spec['output_path'] else None
        row = operational_direct_check_child(spec, original, captured, parent, raw, source, obj)
        if spec['output_path']:
            objects[spec['output_path']] = _operational_api.sha(obj)
        if spec['module'] in owner['audit_names']:
            audits[spec['module']] = operational_direct_exact_axioms(raw.decode(), owner['audit_names'][spec['module']])
        children.append(row)
    _operational_api.require({p.relative_to(output).as_posix() for p in (output / 'build').rglob('*.olean')} == set(objects), 'Original fresh-object census differs')
    _operational_api.require(set(audits) == set(owner['audit_names']), 'Incomplete original audit-stage census')
    metadata = operational_direct_check_metadata(plan, trace, parent, receipt, output, lean) if plan['metadata'] else None
    if packet == 't08-common':
        keys = ['status', 'scientific_manifest_sha256', 'custom_sources_compiled', 'new_theorems_audited', 'mathlib_source_files']
        _operational_api.require(json.loads(parent_text) == {k: receipt[k] for k in keys}, 'Original common terminal stdout differs')
    elif packet == 't08-shared':
        keys = ['status', 'public_manifest_sha256', 'scientific_theorems_audited', 'reviewer_theorems_audited', 'mutants_semantically_rejected']
        _operational_api.require(json.loads(parent_text) == {k: receipt[k] for k in keys}, 'Original shared terminal stdout differs')
        _operational_api.require(receipt['scientific_axioms'] == audits['SuiteAxioms'] and receipt['reviewer_axioms'] == {k: v for name, audit in audits.items() if name != 'SuiteAxioms' for k, v in audit.items()}, 'Original shared axiom table differs from actual logs')
    elif packet == 't08-controller':
        expected = [row['module'] + ' PASS' for row in specs if row['output_path']]
        lines = parent_text.splitlines()
        _operational_api.require(lines[:-1] == expected and json.loads(lines[-1]) == {'status': 'PASS', 'receipt': str(receipt_path)}, 'Original controller terminal stdout differs')
        _operational_api.require(receipt['axiom_audits'] == audits, 'Original controller axiom table differs from actual logs')
    else:
        _operational_api.require(parent_text.splitlines() == [row['module'] + ' PASS' for row in specs if row['module']], 'Original transport terminal stdout differs')
    return {'packet': packet, 'children': children, 'metadata_probe': metadata, 'physical_child_count': plan['physical_child_count'], 'original_receipt_child_count': len(rows), 'trace_sha256': _operational_api._file_hashes(trace), 'original_receipt_sha256': _operational_api.sha(receipt_path.read_bytes()), 'original_driver_sha256': owner['driver_sha256'], 'output_hashes': objects, 'axiom_readbacks': audits, 'required_separate_controls': owner['required_separate_controls'], 'required_post_dependency_readback': plan['required_post_dependency_readback'], 'inherited_only_wrapper_checks': plan['inherited_only_wrapper_checks'], 'scope': 'ORIGINAL_DRIVER_COLLECTION_ONLY_NOT_QUALIFICATION'}

def operational_direct_file_identity(path):
    hasher = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            size += len(block)
            hasher.update(block)
    return (size, hasher.hexdigest())

def operational_direct_verify_dependency_tree(root, pin, exceptions):
    """Read-only full census; exception bytes must come from pinned source data."""
    root = _operational_api.no_symlinks(root).resolve()
    rows = pin['entries']
    names = [_operational_api.relative(row['path']) for row in rows]
    _operational_api.require(len(names) == len(set(names)) and set(exceptions) <= set(names), 'Invalid dependency identity inventory')
    observed = set()
    for name in pin['roots']:
        tree = root if name == '' else _operational_api.path_in(root, name)
        _operational_api.require(tree.is_dir() and (not tree.is_symlink()), 'Missing exact dependency tree')
        if name:
            observed.add(name)
        observed.update((path.relative_to(root).as_posix() for path in tree.rglob('*')))
    _operational_api.require(observed == set(names), 'Dependency entry inventory changed')
    accepted = []
    for row in rows:
        path = root / row['path']
        _operational_api.no_symlinks(path.parent)
        if row['kind'] == 'directory':
            _operational_api.require(path.is_dir() and (not path.is_symlink()), 'Dependency directory changed')
        elif row['kind'] == 'symlink':
            _operational_api.require(path.is_symlink() and os.readlink(path) == row['target'] and path.exists() and path.resolve().is_relative_to(root), 'Dependency symlink differs or escapes root')
        else:
            _operational_api.require(row['kind'] == 'file' and (not path.is_symlink()) and path.is_file() and stat.S_ISREG(path.stat().st_mode), 'Dependency file kind changed')
            size, digest = operational_direct_file_identity(path)
            if size == row['bytes'] and digest == row['sha256']:
                continue
            alternate = exceptions.get(row['path'])
            _operational_api.require(alternate is not None and size == alternate['current_bytes'] and (digest == alternate['current_sha256']), 'Dependency bytes differ from exact source-owned identities')
            accepted.append(row['path'])
    return {'entries': len(rows), 'accepted_metadata_exceptions': accepted, 'exact_inventory': True}

def operational_direct_verify_post_dependencies(packet, root, lean_root, mathlib):
    """Additional after-readback required by the two before-only originals.

    Shared/controller originals already repeat their complete byte checks.
    Their original cache-normalization logic must remain unchanged; the
    public adapter separately retains its ordinary tool/package readback.
    """
    _operational_api.require(packet in {'t08-common', 't09-transport'}, 'This extra readback applies only to before-only originals')
    owner = operational_direct_verify_sources(packet, root)
    root = Path(root)
    mathlib = _operational_api.no_symlinks(mathlib).resolve()
    lean_root = _operational_api.no_symlinks(lean_root).resolve()
    prefix = '' if packet == 't08-common' else 'dependencies/'
    source_manifest = _operational_api.path_in(root, prefix + 'MATHLIB_SOURCE_PIN.json')
    pin = _operational_api.read_json(source_manifest)
    files = pin['files']
    _operational_api.require(len(files) == 6816 and len({row['path'] for row in files}) == 6816, 'Changed Mathlib source census')
    for row in files:
        size, digest = operational_direct_file_identity(_operational_api.path_in(mathlib, row['path']))
        _operational_api.require(size == row.get('bytes', row.get('size')) and digest == row['sha256'], 'Mathlib source changed after original execution')
    result = {'mathlib_source_files': len(files), 'source_manifest_sha256': _operational_api.sha(source_manifest.read_bytes()), 'original_driver_sha256': owner['driver_sha256'], 'dependencies_mutated': False}
    if packet == 't09-transport':
        lean_pin = _operational_api.read_json(root / 'dependencies/LEAN_DISTRIBUTION_PIN.json')
        cache_pin = _operational_api.read_json(root / 'dependencies/MATHLIB_CACHE_PIN.json')
        alternatives = _operational_api.read_json(root / 'dependencies/CACHE_METADATA_EXCEPTION_PINS.json')['files']
        _operational_api.require(len(alternatives) == len({row['path'] for row in alternatives}), 'Duplicate source-owned cache alternative')
        result['lean'] = operational_direct_verify_dependency_tree(lean_root, lean_pin, {})
        result['cache'] = operational_direct_verify_dependency_tree(mathlib, cache_pin, {row['path']: row for row in alternatives})
        result['byte_scope'] = 'EXACT_ORIGINAL_DISTRIBUTION_CACHE_AND_SOURCE_PINS'
    else:
        result['byte_scope'] = 'ALL_ORIGINAL_SOURCE_PINS_WITH_INHERITED_OFFICIAL_CACHE_TRUST'
    return result
