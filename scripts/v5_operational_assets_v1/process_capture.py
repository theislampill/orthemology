def _operational_popen_require(condition, message):
    if not condition:
        raise ValueError(message)

def _operational_popen_sha(_operational_popen_raw):
    return hashlib.sha256(_operational_popen_raw).hexdigest()

def _operational_popen_utc():
    return _operational_datetime.datetime.now(_operational_datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def _operational_popen_no_symlinks(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        _operational_popen_require(not part.is_symlink(), 'Symlink in private capture path')
    return path

def _operational_popen_raw(value):
    if value is None:
        return b''
    return value.encode('utf-8') if isinstance(value, str) else value

class _operational_popen__CapturedProcess:

    def __init__(self, process, record, directory, contract):
        self.process = process
        self.record = record
        self.directory = directory
        self.contract = contract
        self.timed_out = False
        self.completed = False
        self.stdout = b''
        self.stderr = b''

    @property
    def pid(self):
        return self.process.pid

    @property
    def returncode(self):
        return self.process.returncode

    def poll(self):
        return self.process.poll()

    def save(self):
        stem = f"{self.record['index']:04}"
        (self.directory / (stem + '.log')).write_bytes(self.stdout + self.stderr)
        self.record['log_sha256'] = _operational_popen_sha(self.stdout + self.stderr)
        (self.directory / (stem + '.json')).write_text(json.dumps(self.record, indent=2) + '\n')

    def finish_capture(self, stdout, stderr, terminal):
        self.stdout, self.stderr = (_operational_popen_raw(stdout), _operational_popen_raw(stderr))
        hashes = {}
        for name in self.contract['output_paths']:
            path = _operational_popen_no_symlinks(name)
            if path.is_file():
                hashes[name] = _operational_popen_sha(path.read_bytes())
        self.record.update(ended_at=_operational_popen_utc(), terminal=terminal, exit_code=self.process.returncode, output_hashes=hashes)
        self.completed = True
        self.save()

    def communicate(self, input=None, timeout=None):
        _operational_popen_require(input is None and (not self.completed), 'Unreviewed repeated communicate or input')
        position = len(self.record['communicate_timeouts'])
        _operational_popen_require(position < len(self.contract['timeouts']) and timeout == self.contract['timeouts'][position] and (timeout is None or type(timeout) in (int, float)), 'Changed original communicate timeout')
        self.record['communicate_timeouts'].append(timeout)
        self.save()
        try:
            stdout, stderr = self.process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            self.timed_out = True
            self.stdout, self.stderr = (_operational_popen_raw(error.stdout), _operational_popen_raw(error.stderr))
            self.record['terminal'] = 'TIMEOUT_WAITING_FOR_ORIGINAL_REAP'
            self.save()
            raise
        except BaseException as error:
            self.record['communicate_exception'] = type(error).__name__
            self.save()
            raise
        terminal = 'TIMEOUT' if self.timed_out else 'INTERRUPTED' if self.process.returncode < 0 else 'COMPLETED'
        self.finish_capture(stdout, stderr, terminal)
        return (stdout, stderr)

    def cleanup(self, reason):
        if self.completed:
            return
        self.record['cleanup_reason'] = reason
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            stdout, stderr = self.process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = self.process.communicate()
        self.finish_capture(stdout, stderr, 'TIMEOUT' if self.timed_out else 'INTERRUPTED')

class _operational_popen_PopenCapture:
    """Serial source-call capture with cleanup when original code unwinds.

    This records facts, not control success. Negative exit codes, timeouts,
    missing objects and incomplete plans cannot be promoted by finish().
    """

    def __init__(self, original_popen, trace, commands):
        _operational_popen_require(isinstance(commands, list) and commands, 'Missing source command plan')
        _operational_popen_require(len({r['id'] for r in commands}) == len(commands), 'Duplicate child id')
        self.commands = copy.deepcopy(commands)
        self.original_popen = original_popen
        self.trace = _operational_popen_no_symlinks(trace)
        _operational_popen_require(not self.trace.exists(), 'Capture output must be absent')
        for row in self.commands:
            _operational_popen_require(set(row) <= {'id', 'argv', 'cwd', 'cwd_mode', 'timeouts', 'source_hashes', 'output_paths', 'transport_argv'}, 'Unreviewed capture plan field')
            for argv in [row['argv']] + ([row['transport_argv']] if 'transport_argv' in row else []):
                _operational_popen_require(isinstance(argv, list) and argv and all((isinstance(x, str) and x and ('\x00' not in x) for x in argv)), 'Malformed argv')
            _operational_popen_require(row['cwd_mode'] in {'EXPLICIT', 'INHERITED'} and Path(row['cwd']).is_absolute(), 'Unbound cwd')
            _operational_popen_require(isinstance(row['timeouts'], list) and row['timeouts'] and (row['timeouts'][0] is not None), 'Missing initial source timeout')
            _operational_popen_require(all((x is None or (type(x) in (int, float) and math.isfinite(x) and (0 < x <= 86400)) for x in row['timeouts'])), 'Invalid source timeout')
            _operational_popen_require(isinstance(row['source_hashes'], dict) and isinstance(row['output_paths'], list), 'Malformed source bindings')
        self.trace.mkdir(parents=True)
        self.processes = []

    def __enter__(self):
        self.previous_sigterm = signal.getsignal(signal.SIGTERM)

        def interrupted(signum, frame):
            raise KeyboardInterrupt('Owning adapter requested process-group cleanup')
        signal.signal(signal.SIGTERM, interrupted)
        return self

    def __exit__(self, kind, value, traceback):
        try:
            for process in self.processes:
                process.cleanup(kind.__name__ if kind else 'UNFINISHED_ORIGINAL_CHILD')
        finally:
            signal.signal(signal.SIGTERM, self.previous_sigterm)
        return False

    def __call__(self, argv, *args, **kwargs):
        index = len(self.processes)
        _operational_popen_require(not args and index < len(self.commands) and (argv == self.commands[index]['argv']), 'Unreviewed or repeated original command')
        _operational_popen_require(all((p.completed for p in self.processes)), 'Original process calls must be serial')
        row = self.commands[index]
        keys = {'env', 'text', 'stdout', 'stderr', 'start_new_session'}
        if row['cwd_mode'] == 'EXPLICIT':
            keys.add('cwd')
        _operational_popen_require(set(kwargs) == keys and isinstance(kwargs['env'], dict), 'Changed original Popen kwargs')
        _operational_popen_require(kwargs['text'] is True and kwargs['stdout'] == subprocess.PIPE and (kwargs['stderr'] == subprocess.STDOUT) and (kwargs['start_new_session'] is True), 'Changed original stream or process-group form')
        cwd = _operational_popen_no_symlinks(kwargs['cwd'] if 'cwd' in kwargs else Path.cwd())
        _operational_popen_require(str(cwd) == row['cwd'], 'Changed original cwd')
        for name, expected in row['source_hashes'].items():
            path = _operational_popen_no_symlinks(name)
            _operational_popen_require(path.is_file() and _operational_popen_sha(path.read_bytes()) == expected, 'Original source changed before launch')
        for name in row['output_paths']:
            _operational_popen_require(not _operational_popen_no_symlinks(name).exists(), 'Original output already exists')
        actual = row.get('transport_argv', argv)
        record = {'index': index, 'source_child_id': row['id'], 'source_argv': argv, 'argv': actual, 'argv_translation': actual != argv, 'cwd': str(cwd), 'cwd_mode': row['cwd_mode'], 'source_hashes': row['source_hashes'], 'environment_sha256': _operational_popen_sha(json.dumps(kwargs['env'], sort_keys=True).encode()), 'started_at': _operational_popen_utc(), 'ended_at': None, 'terminal': 'RUNNING', 'exit_code': None, 'communicate_timeouts': [], 'output_hashes': {}, 'log_sha256': _operational_popen_sha(b'')}
        process = self.original_popen(actual, **kwargs)
        record['pid'] = process.pid
        captured = _operational_popen__CapturedProcess(process, record, self.trace, row)
        self.processes.append(captured)
        captured.save()
        return captured

    def finish(self):
        _operational_popen_require(len(self.processes) == len(self.commands), 'Original physical child census is incomplete')
        _operational_popen_require(all((p.completed and p.record['terminal'] == 'COMPLETED' for p in self.processes)), 'Original physical child terminal is incomplete, timed out or interrupted')

def _operational_nested_adapter():
    return _operational_api
def _operational_nested_run_without_outer_popen(original_run, original_popen):
    """Only for reviewed serial drivers: keep run's implementation unmodified.

    subprocess.run internally resolves subprocess.Popen at call time. The
    companion's one nested-launch interception must not also consume these
    direct compiler calls; they have their own complete capture ledger.
    """

    def invoke(*args, **kwargs):
        installed = subprocess.Popen
        try:
            subprocess.Popen = original_popen
            return original_run(*args, **kwargs)
        finally:
            subprocess.Popen = installed
    return invoke

def _operational_nested_bound_run(original_run, trace, specs):
    _operational_api = _operational_nested_adapter()
    commands = [{k: row[k] for k in ('argv', 'cwd', 'timeout')} for row in specs]
    captured = _operational_api.operational_traced_run(original_run, trace, commands)
    position = 0

    def invoke(argv, *args, **kwargs):
        nonlocal position
        require(position < len(specs) and argv == specs[position]['argv'], 'Changed source-owned nested child')
        row = specs[position]
        if row['binding_kind'] == 'TOOL_PROBE':
            require(sha(no_symlinks(argv[0]).read_bytes()) == row['tool_sha256'], 'Nested tool probe changed')
        else:
            body = no_symlinks(row['actual_source_path']).read_bytes()
            if row['binding_kind'] == 'GENERATED_BY_ORIGINAL':
                require(body == row['generated_text'].encode() and sha(body) == row['generated_source_sha256'], 'Nested original-generated source changed')
            else:
                require(row['binding_kind'] == 'ORIGINAL_SOURCE' and sha(body) == row['source_sha256'], 'Nested original source changed')
        position += 1
        return captured(argv, *args, **kwargs)

    def finish():
        require(position == len(specs), 'Nested physical child census incomplete')
        captured.finish()
    invoke.finish = finish
    return invoke
