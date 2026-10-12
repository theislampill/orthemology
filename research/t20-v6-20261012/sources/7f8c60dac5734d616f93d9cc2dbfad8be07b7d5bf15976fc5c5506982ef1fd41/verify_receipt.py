import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent.parent
folder=pathlib.Path(__file__).resolve().parent
receipt=json.loads((folder/'REVIEW_RECEIPT.json').read_text())
for group in ['author_files','review_files','retained_inputs']:
    for name,expected in receipt[group].items():
        actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
        assert actual==expected,(name,actual,expected)
run=subprocess.run([sys.executable,str(folder/'check_review.py')],check=True,capture_output=True,text=True)
assert json.loads(run.stdout)==json.loads((folder/'INDEPENDENT_CONTROLS.json').read_text())
print('PASS: final author/review/input hashes match; independent exact controls replay unchanged.')
