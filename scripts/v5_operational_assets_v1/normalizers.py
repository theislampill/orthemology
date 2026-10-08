def operational_output_strict_equal(actual, expected):
    return type(actual) is type(expected) and actual == expected

def operational_output_audit(text, expected_count, expected_names=None):
    records = {}
    for name, raw in re.findall("'([^']+)' depends on axioms:\\s*\\[([^]]*)\\]", text, re.S):
        require(name not in records, 'Duplicate original axiom target')
        records[name] = sorted({x.strip() for x in raw.split(',') if x.strip()})
        require(set(records[name]) <= AXIOMS, 'Unapproved original axiom')
    for name in re.findall("'([^']+)' does not depend on any axioms", text):
        require(name not in records, 'Duplicate original axiom target')
        records[name] = []
    require(len(records) == expected_count, 'Wrong original axiom target count')
    if expected_names is not None:
        require(set(records) == set(expected_names), 'Wrong original axiom target names')
    return records

def operational_output_normalize(packet, source_roots, output, physical_stage, contract_path, *, raw_logs=None):
    """Return source-bound child terminal/log records without creating evidence.

    source_roots maps original archive SHA to its freshly extracted exact root.
    raw_logs maps child IDs to paths of actual unmodified tracer-captured logs;
    it is required for the T09 path-projected original wrapper.
    """
    require(packet in OPERATIONAL_DRIVER_SHA, 'Unreviewed original suite')
    require(physical_stage.get('terminal') == 'COMPLETED' and type(physical_stage.get('exit_code')) is int and (physical_stage['exit_code'] == 0), 'Physical parent did not complete successfully')
    contract = _OPERATIONAL_DATA['packets'][packet]['original_contract']
    def member_path(meta):
        root = source_roots[meta['parent_archive_sha256']]
        return operational_output_file(root, meta['member_chain'][-1])
    require(sha(member_path(contract['driver']).read_bytes()) == OPERATIONAL_DRIVER_SHA[packet], 'Wrong actual original driver bytes')
    receipt = operational_output_read_json(output, contract['receipt'])
    require(receipt['status'] == contract['terminal_status'], 'Original full suite did not reach its terminal receipt')
    for key, value in contract['required_receipt_fields'].items():
        require(operational_output_strict_equal(receipt.get(key), value), 'Original terminal field changed: ' + key)
    receipts = {contract['receipt']: receipt}
    stages = []
    objects = {}
    audits = {}
    source_hashes = {}
    groups = {}
    for c in contract['stages']:
        groups.setdefault((c['receipt'], c['receipt_table'], c['receipt_stage_key']), []).append(c['receipt_stage_name'])
    for (receipt_path, table, key), names in groups.items():
        if receipt_path not in receipts:
            receipts[receipt_path] = operational_output_read_json(output, receipt_path)
        observed = [x[key] for x in receipts[receipt_path][table]]
        expected = ['compiler_version'] + names if packet == 't08-batch' and receipt_path == 'fresh science/RECEIPT.json' else names
        require(observed == expected, 'Missing/reordered original stages in ' + receipt_path)
    for c in contract['stages']:
        rows = receipts[c['receipt']][c['receipt_table']]
        row = next((x for x in rows if x[c['receipt_stage_key']] == c['receipt_stage_name']))
        require(type(row['exit_code']) is int and row['exit_code'] == c['expected_exit'], 'Original child exit differs: ' + c['id'])
        require(row.get('timed_out', False) is False, 'Timed-out original child has no semantic credit')
        text, log_sha = operational_output_log(output, c['log_path'])
        recorded = row.get('log_sha256', row.get('projected_log_sha256'))
        require(recorded == log_sha, 'Original child log digest differs: ' + c['id'])
        if c['source'] is not None:
            meta = c['source']
            actual = sha(member_path(meta).read_bytes())
            require(actual == meta['sha256'], 'Original child source changed')
            if 'source_sha256' in row:
                require(row['source_sha256'] == actual, 'Child receipt source association changed')
            source_hashes[c['source']['selector']] = actual
        if c['expected_exit']:
            require('error:' in text and (not OPERATIONAL_INFRA.search(text)), 'Infrastructure/resource failure is not intended rejection')
            if c['role'] == 'NONEXECUTABILITY_BOUNDARY':
                require(c['source']['sha256'] == OPERATIONAL_NONEXEC_SOURCE_SHA and c['id'] == 'baseline/PredecessorCallableFailure', 'Unreviewed nonexecutability exception')
                require('which has no executable code' in text, 'Wrong predecessor nonexecutability diagnostic')
            for literal in c.get('required_literals', []):
                require(literal in text, 'Missing source-prescribed diagnostic')
            for pattern in c.get('required_regexes', []):
                require(re.search(pattern, text, re.S) is not None, 'Missing source-prescribed diagnostic pattern')
            if 'classification' in c:
                require(row.get('classification') == c['classification'], 'Wrong original mutant classification')
        else:
            require('sorryAx' not in text and 'error:' not in text, 'Positive child has a proof/error diagnostic')
            if 'warning:' in text:
                require(packet == 't08-shared' and c['module'] == 'ReviewerControls' and (row.get('accepted_exact_historical_lint_count') == 2), 'Unapproved positive warning')
                require(c['source']['sha256'] == contract['lint_exception']['source']['sha256'], 'Changed warning-exception source')
                require(text.count('warning:') == 2 and all((loc + ': warning:' in text for loc in contract['lint_exception']['locations'])), 'Changed exact warning locations/count')
        raw_sha = None
        if packet == 't09-controller':
            require(raw_logs is not None and c['id'] in raw_logs, 'Actual original raw child stream required')
            raw = Path(raw_logs[c['id']]).read_bytes()
            raw_sha = sha(raw)
            require(raw_sha == row['raw_stdout_sha256'], 'Actual raw child log identity differs')
        obj = c.get('fresh_object_path')
        if obj:
            actual = sha(operational_output_file(output, obj).read_bytes())
            recorded_obj = row.get('object_sha256', row.get('olean_sha256'))
            if recorded_obj is not None:
                require(recorded_obj == actual, 'Original child object changed')
            objects[obj] = actual
        stages.append({'id': c['id'], 'terminal': 'COMPLETED', 'exit_code': row['exit_code'], 'log_relative_path': c['log_path'], 'log_sha256': raw_sha or log_sha, 'original_projected_log_sha256': log_sha if raw_sha else None, 'actual_recorded_argv': row.get('command'), 'actual_recorded_cwd': row.get('compiler_cwd'), 'first_run_tracer_required': True, 'outcome': 'REJECT' if c['expected_exit'] else 'ACCEPT'})
    if packet == 't08-common':
        audits['AllAxioms'] = operational_output_audit(operational_output_log(output, 'logs/AllAxioms.log')[0], 352)
    elif packet == 't08-batch':
        nested = receipts['fresh science/RECEIPT.json']
        require(receipt['source_replay_receipt_sha256'] == sha(operational_output_file(output, 'fresh science/RECEIPT.json').read_bytes()), 'Nested physical run receipt binding differs')
        require(nested['status'] == 'PASS' and nested['custom_source_modules'] == 61 and (nested['named_declarations_audited'] == 902) and (nested['author_theorems_audited'] == 476), 'Incomplete single nested scientific replay')
        require(nested['dependencies_checked_before_after'] is True and nested['dependencies_mutated'] is False, 'Nested dependency after readback absent')
        audits['AllNamedDeclarations'] = operational_output_audit(operational_output_log(output, 'fresh science/logs/AllNamedDeclarations.log')[0], 902, nested['declaration_axioms'])
        audits['ReviewerNamedDeclarations'] = operational_output_audit(operational_output_log(output, 'logs/ReviewerNamedDeclarations.log')[0], 78, receipt['reviewer_axioms'])
    elif packet == 't08-shared':
        audits['SuiteAxioms'] = operational_output_audit(operational_output_log(output, 'logs/SuiteAxioms.log')[0], 88, receipt['scientific_axioms'])
        require(len(receipt['reviewer_axioms']) == 18, 'Wrong reviewer axiom inventory')
    elif packet == 't08-controller':
        for name, n in [('AllScientificAxioms', 129), ('AllReviewerAxioms', 20)]:
            audits[name] = operational_output_audit(operational_output_log(output, 'logs/' + name + '.log')[0], n, receipt['axiom_audits'][name])
    elif packet == 't09-controller':
        expected = json.loads(member_path(contract['expected_native_results']).read_bytes())
        for name, value in expected['compiled_projections'].items():
            require(operational_output_log(output, 'logs/' + name + '.log')[0].strip() == value, 'Changed actual compiled projection')
        require(operational_output_log(output, 'logs/NativeExecutionChecks.log')[0].splitlines() == expected['author_runtime_lines'], 'Missing/reordered 13 author runtime outcomes')
        require(operational_output_log(output, 'logs/ordered__OrderedExecutionControls.log')[0].splitlines() == expected['independent_runtime_lines'], 'Missing/reordered 8 reviewer runtime outcomes')
        for c in contract['stages']:
            if 'exact_axiom_name_inventory' in c:
                names = json.loads(member_path(c['exact_axiom_name_inventory']).read_bytes())
                audits[c['id']] = operational_output_audit(operational_output_log(output, c['log_path'])[0], len(names), names)
        for before, after in [('lean_pin', 'post_lean_pin'), ('mathlib_source_pin', 'post_mathlib_source_pin'), ('mathlib_cache_pin', 'post_mathlib_cache_pin')]:
            require(receipt[before] == receipt[after], 'Original dependency identity changed')
    else:
        for name, n in contract['named_audit_counts'].items():
            c = next((c for c in contract['stages'] if c.get('module') == name))
            audits[name] = operational_output_audit(operational_output_log(output, c['log_path'])[0], n)
    return {'physical_suite': packet, 'original_driver_sha256': OPERATIONAL_DRIVER_SHA[packet], 'original_receipt_sha256': sha(operational_output_file(output, contract['receipt']).read_bytes()), 'stages': stages, 'actual_output_hashes': objects, 'original_axiom_readbacks': audits, 'source_hashes_after': source_hashes, 'required_additional_controls': contract.get('additional_controls', {}), 'scope': 'Actual complete original driver output; wrapper controls, first-run trace association and safe target closure are separate mandatory adapter checks.'}

