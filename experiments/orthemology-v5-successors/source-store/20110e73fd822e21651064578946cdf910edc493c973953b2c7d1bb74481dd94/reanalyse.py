#!/usr/bin/env python3
"""Portable local-file reanalysis; only aggregate JSON is written."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy import stats

import fit_bfgs
import fit_checked

HERE = Path(__file__).resolve().parent
LEVELS = np.array([-.15, -.07, -.035, -.015, .015, .035, .07, .15])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checked_bytes(path, expected_hash):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected_hash, 'Source SHA-256 mismatch')
    return raw


def paired(ind, inf):
    ind, inf = np.asarray(ind, float), np.asarray(inf, float)
    require(ind.ndim == 1 and ind.shape == inf.shape and len(ind) > 1,
            'Paired vectors must have matching nontrivial shape')
    require(np.isfinite(ind).all() and np.isfinite(inf).all(), 'Nonfinite paired value')
    d = inf-ind
    require(d.std(ddof=1) > 0, 'Degenerate paired differences')
    result = stats.ttest_rel(inf, ind)
    ci = stats.t.interval(.95, len(d)-1, loc=d.mean(), scale=stats.sem(d))
    return {'paired_dyads':len(d), 'IND_mean':float(ind.mean()), 'INF_mean':float(inf.mean()),
            'INF_minus_IND_mean':float(d.mean()), 't':float(result.statistic), 'df':len(d)-1,
            'p_two_sided':float(result.pvalue), 'difference_CI95':list(map(float, ci))}


def aggregate_template():
    return dict.fromkeys(('paired_dyads', 'IND_mean', 'INF_mean', 'INF_minus_IND_mean',
                          't', 'df', 'p_two_sided', 'difference_CI95',
                          'workbook_reconciliation_4dp'))


def channels(a, b):
    require(a.shape == (128,19) and b.shape == (128,11), 'Unexpected matrix shape')
    for matrix in (a, b):
        require(np.isfinite(matrix[:,3:5]).all(), 'Missing task contrast or interval')
        require(np.isin(matrix[:,3], [1,2]).all(), 'Invalid target interval')
        require(np.isin(matrix[:,4], [.015,.035,.07,.15]).all(), 'Invalid contrast magnitude')
    xi, xf = a[:,4]*(2*a[:,3]-3), b[:,4]*(2*b[:,3]-3)
    for x in (xi, xf):
        levels, counts = np.unique(x, return_counts=True)
        require(np.array_equal(levels, LEVELS) and np.all(counts == 16), 'Unbalanced source contrast bins')
    kb, ms, ji = ((np.sign(a[:,column])+1)/2 for column in (7,10,13))
    jf = b[:,9]-1
    for y in (kb, ms, ji, jf):
        require(np.isfinite(y).all() and np.isin(y, [0.,1.]).all(), 'Invalid selected response')
    for y, interval_column, correctness_column in ((kb,9,8),(ms,12,11),(ji,15,14)):
        require(np.array_equal(y+1, a[:,interval_column]), 'IND response mapping mismatch')
        require(np.array_equal(y+1 == a[:,3], a[:,correctness_column]), 'IND correctness mismatch')
    require(np.array_equal(jf, (np.sign(b[:,7])+1)/2), 'INF response mapping mismatch')
    require(np.array_equal(jf+1 == b[:,3], b[:,8]), 'INF correctness mismatch')
    agreement = kb == ms
    require(np.array_equal(ji[agreement], kb[agreement]), 'Agreement response mismatch')
    require(np.array_equal(np.isnan(a[:,18]), agreement), 'Timing missingness mismatch')
    # Timing is checked but is never used to filter the response observations.
    curves = {'kb_private':(xi,kb), 'ms_private':(xi,ms), 'joint_IND':(xi,ji),
              'joint_INF':(xf,jf), 'kb_joint_IND':(xi[::2],ji[::2]),
              'ms_joint_IND':(xi[1::2],ji[1::2]), 'kb_joint_INF':(xf[::2],jf[::2]),
              'ms_joint_INF':(xf[1::2],jf[1::2])}
    return curves, int(np.count_nonzero(~agreement))


def reconstruct(ind, inf, summary, fitter):
    rows = []
    for i, (a,b) in enumerate(zip(ind,inf)):
        curves, disagreements = channels(a,b)
        require(disagreements == summary[i,8], 'Disagreement count mismatch')
        fitted = {name:fitter(x,y) for name,(x,y) in curves.items()}
        values = {name:item['sensitivity'] for name,item in fitted.items()}
        low, high = ('ms','kb') if values['ms_private'] < values['kb_private'] else ('kb','ms')
        row = [values[f'{low}_private'], values[f'{low}_joint_IND'], values[f'{low}_joint_INF'],
               values[f'{high}_private'], values[f'{high}_joint_IND'], values[f'{high}_joint_INF'],
               values['joint_IND'], values['joint_INF']]
        rows.append(row)
    return np.asarray(rows)


def run(decisions_zip, summary_xlsx):
    metadata = json.loads((HERE/'INPUTS.json').read_text(encoding='utf-8'))
    source = metadata['required_inputs']
    zip_bytes = checked_bytes(decisions_zip, source['decisions_zip']['sha256'])
    xlsx_bytes = checked_bytes(summary_xlsx, source['summary_xlsx']['sha256'])
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        member = metadata['runtime_read_scope']['archive_member']
        mat = archive.read(member['name'])
        require(hashlib.sha256(mat).hexdigest() == member['sha256'], 'MAT SHA-256 mismatch')
        data = loadmat(io.BytesIO(mat), simplify_cells=True)
    with pd.ExcelFile(io.BytesIO(xlsx_bytes)) as book:
        sheet = pd.read_excel(book, sheet_name='Experiment 2', header=None)
        require(sheet.shape == (17,9), 'Unexpected workbook range')
        require(pd.read_excel(book, sheet_name='Sheet3', header=None).empty, 'Unexpected auxiliary sheet')
    summary = sheet.iloc[2:17,:9].to_numpy(dtype=float)
    require(np.isfinite(summary).all(), 'Missing workbook value')
    ind = [item['dyaddata'] for item in data['DataIND']]
    inf = [item['dyaddata'] for item in data['DataINF']]
    require(len(ind) == len(inf) == 15, 'Expected paired source structures')
    a = reconstruct(ind,inf,summary,fit_bfgs.fit)
    b = reconstruct(ind,inf,summary,fit_checked.fit)
    max_difference = float(np.max(np.abs(a-b)))
    require(max_difference < 1e-6, 'Cross-implementation disagreement')
    require(np.array_equal(np.round(a,4), summary[:,:8]), 'BFGS workbook reconciliation failed')
    require(np.array_equal(np.round(b,4), summary[:,:8]), 'Checked workbook reconciliation failed')
    require(np.count_nonzero(b[:,0] < 0) == 1, 'Negative-slope preservation check failed')
    result = paired(b[:,6], b[:,7])
    result['workbook_reconciliation_4dp'] = True
    require(set(result) == set(aggregate_template()), 'Aggregate output contract mismatch')
    # Keep estimates in memory only. The public interface exposes no row output.
    return result, {'status':'pass', 'max_abs_sensitivity_difference':max_difference}


def validate_output(output, inputs):
    if output is not None:
        path = Path(output)
        for item in inputs:
            source = Path(item)
            require(path.resolve() != source.resolve(), 'Output must not overwrite an input')
            if path.exists() and source.exists():
                require(not path.samefile(source), 'Output must not overwrite an input')


def write_aggregate(result, output, inputs):
    validate_output(output, inputs)
    text = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if output is None:
        sys.stdout.write(text)
    else:
        Path(output).write_text(text, encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decisions-zip', required=True, type=Path, help='Local, separately obtained ZIP')
    parser.add_argument('--summary-xlsx', required=True, type=Path, help='Local, separately obtained workbook')
    parser.add_argument('--output', type=Path, help='Aggregate JSON destination; default is stdout')
    args = parser.parse_args(argv)
    try:
        validate_output(args.output, (args.decisions_zip,args.summary_xlsx))
        result, _ = run(args.decisions_zip, args.summary_xlsx)
        write_aggregate(result, args.output, (args.decisions_zip,args.summary_xlsx))
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(2, f'Analysis failed: {error}\n')


if __name__ == '__main__':
    main()
