#!/usr/bin/env python3
"""Verify public payload membership and byte identity only.

No source workspace, network, private capture, toolchain, or imported research
module is required. A PASS is not source authentication, scholarly acceptance,
formal-proof replay, signature verification, or release authorisation.
V2 additionally checks a declared separate-report binding. Only --report reads
the actual report bytes; payload-only verification explicitly leaves it unchecked.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MANIFEST='SELECTION_MANIFEST.json'

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=value
    return result

def safe_path(value):
    if not isinstance(value,str) or not value or '\\' in value or ':' in value or '\x00' in value:
        return False
    path=PurePosixPath(value)
    return not path.is_absolute() and str(path)==value and all(p not in ('','.','..') for p in value.split('/'))

def digest(data):return hashlib.sha256(data).hexdigest()

def identity_record(value, name_key='path'):
    return (isinstance(value,dict) and safe_path(value.get(name_key))
            and type(value.get('bytes')) is int and value['bytes'] >= 0
            and isinstance(value.get('sha256'),str)
            and re.fullmatch('[0-9a-f]{64}',value['sha256']) is not None)

def report_binding(manifest, wanted, actual):
    declared=manifest.get('report_binding')
    if not identity_record(declared):raise ValueError('missing or invalid report binding')
    name=declared['path']
    row=wanted.get(name)
    if row is None or name not in actual:raise ValueError('report binding is not a selected file')
    if any(declared[k]!=row[k] for k in ('bytes','sha256')):raise ValueError('report binding identity is stale')
    raw=actual[name].read_bytes()
    if len(raw)!=declared['bytes'] or digest(raw)!=declared['sha256']:raise ValueError('report binding identity differs from actual bytes')
    value=json.loads(raw,object_pairs_hook=unique_object)
    if not isinstance(value,dict) or value.get('schema')!='tenth-separate-report-binding-v1' or value.get('distribution')!='separate_native_docx_identity_only':
        raise ValueError('invalid report binding contract')
    report=value.get('report')
    if not identity_record(report,'filename') or '/' in report['filename'] or not report['filename'].endswith('.docx'):
        raise ValueError('invalid report identity')
    claim=value.get('claim_map')
    if not identity_record(claim) or claim['path'] not in wanted or claim['path'] not in actual:
        raise ValueError('claim map is not a selected file')
    if any(claim[k]!=wanted[claim['path']][k] for k in ('bytes','sha256')):raise ValueError('claim map identity is stale')
    return value

def verify(root, expected_manifest=None, report=None, require_report=False):
    errors=[]
    if root.is_symlink():return {'status':'FAIL','errors':['symlink bundle root'],'files_checked':0}
    if not root.is_dir():return {'status':'FAIL','errors':['bundle root is not a directory'],'files_checked':0}
    manifest_path=root/MANIFEST
    if manifest_path.is_symlink():return {'status':'FAIL','errors':['symlink manifest'],'files_checked':0}
    try:
        if not stat.S_ISREG(manifest_path.stat().st_mode):raise ValueError('manifest is not a regular file')
        raw=manifest_path.read_bytes();manifest_sha=digest(raw)
        if expected_manifest is not None and manifest_sha!=expected_manifest:
            errors.append('manifest sha256 mismatch')
        manifest=json.loads(raw,object_pairs_hook=unique_object)
        if not isinstance(manifest,dict):raise ValueError('manifest must be an object')
        if (manifest.get('schema'),manifest.get('status')) not in [('tenth-public-selection-v2','RELEASE_CANDIDATE'),('tenth-public-selection-v2','FINAL_CANDIDATE'),('tenth-public-selection-v2','FINAL')]:raise ValueError('unsupported schema/status pair')
        if manifest.get('manifest_exclusions')!=[MANIFEST]:raise ValueError('manifest exclusions must contain only '+MANIFEST)
        records=manifest.get('files')
        if not isinstance(records,list) or not records:raise ValueError('files must be a nonempty list')
    except (OSError,ValueError,TypeError) as error:
        return {'status':'FAIL','errors':errors+[str(error)],'files_checked':0}
    wanted={}
    for row in records:
        if not isinstance(row,dict):errors.append('file entry is not an object');continue
        name=row.get('path')
        if not safe_path(name):errors.append('unsafe path: '+repr(name));continue
        if name==MANIFEST:errors.append('manifest cannot include itself');continue
        if name in wanted:errors.append('duplicate path: '+name);continue
        size=row.get('bytes');sha=row.get('sha256')
        if type(size) is not int or size<0:errors.append('invalid bytes: '+name);continue
        if not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{64}',sha):errors.append('invalid sha256: '+name);continue
        wanted[name]=row
    actual={}
    def walk_error(error):errors.append('directory read failed: '+str(error))
    for directory,dirs,files in os.walk(root,followlinks=False,onerror=walk_error):
        for name in list(dirs):
            path=Path(directory)/name
            if path.is_symlink():
                errors.append('symlink directory: '+path.relative_to(root).as_posix());dirs.remove(name)
        for name in files:
            path=Path(directory)/name;relative=path.relative_to(root).as_posix()
            if path.is_symlink():errors.append('symlink file: '+relative);continue
            try:
                if not stat.S_ISREG(path.stat().st_mode):errors.append('nonregular file: '+relative);continue
            except OSError as error:errors.append('file stat failed: '+str(error));continue
            if relative!=MANIFEST:actual[relative]=path
    checked=0
    for name,row in wanted.items():
        if name not in actual:errors.append('missing file: '+name);continue
        try:
            # Files are read only after the complete path/symlink membership scan.
            data=actual[name].read_bytes()
            if len(data)!=row['bytes']:errors.append('size mismatch: '+name)
            if digest(data)!=row['sha256']:errors.append('sha256 mismatch: '+name)
            checked+=1
        except OSError as error:errors.append('file read failed: '+str(error))
    for name in sorted(set(actual)-set(wanted)):errors.append('unlisted file: '+name)
    external={'status':'NOT_CHECKED','reason':'No external report bytes checked; payload-only scope'}
    binding=None
    if manifest['status'] in ('FINAL_CANDIDATE','FINAL') or 'report_binding' in manifest or report is not None or require_report:
        try:binding=report_binding(manifest,wanted,actual)
        except (OSError,ValueError,TypeError) as error:errors.append(str(error))
    if require_report and report is None:errors.append('--report is required for combined verification')
    if report is not None:
        external={'status':'FAIL','path':str(report)}
        if binding is not None:
            try:
                if report.is_symlink():raise ValueError('symlink external report')
                if not stat.S_ISREG(report.stat().st_mode):raise ValueError('external report is not a regular file')
                raw=report.read_bytes();got={'bytes':len(raw),'sha256':digest(raw)}
                external.update(got)
                if any(got[k]!=binding['report'][k] for k in ('bytes','sha256')):raise ValueError('external report size/hash mismatch')
                external['status']='PASS'
            except (OSError,ValueError) as error:errors.append('external report: '+str(error))
    return {'status':'FAIL' if errors else 'PASS','scope':'public file membership, byte identity and declared report binding; no release or scholarly authorisation','release_status':manifest['status'],'manifest_sha256':manifest_sha,'files_checked':checked,'binding_checked':binding is not None,'external_report':external,'combined_report_verification':external['status']=='PASS' and not errors,'errors':errors}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',nargs='?',type=Path,default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--report',type=Path,help='Explicit separate DOCX path; no metadata paths are followed')
    parser.add_argument('--require-report',action='store_true',help='Fail if no --report is supplied')
    args=parser.parse_args()
    result=verify(args.directory,args.expected_manifest_sha256,args.report,args.require_report)
    print(json.dumps(result,indent=2))
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
