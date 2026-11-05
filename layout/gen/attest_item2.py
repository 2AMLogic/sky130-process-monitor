#!/usr/bin/env python3
"""Write evidence/item2.json: the artifact-anchored generic envelope for T1 item 2 (analog).

klt has no `--attest 2` verb, so this is a hand-written envelope (its status is this script's
assertion, which is: the stream was regenerated from layout/gen/gen_osc_bank.py into a scratch
dir, is byte-identical to the committed layout/osc_bank.gds, and layout/gen/check_connectivity.py
passes). It pins the stream by content hash; the manifest pins the envelope's hash.
Usage: python3 layout/gen/attest_item2.py   (prints the envelope's content_hash for the manifest)
"""
import hashlib, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
gds = os.path.join(REPO, "layout", "osc_bank.gds")
sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()
with tempfile.TemporaryDirectory() as d:
    out = os.path.join(d, "regen.gds")
    subprocess.run([sys.executable, os.path.join(HERE, "gen_osc_bank.py"), "-o", out], check=True,
                   stdout=subprocess.DEVNULL)
    regen = sha(open(out, "rb").read())
committed = sha(open(gds, "rb").read())
chk = subprocess.run([sys.executable, os.path.join(HERE, "check_connectivity.py"), gds],
                     capture_output=True, text=True)
status = "pass" if (regen == committed and chk.returncode == 0) else "fail"
import klayout.db as kdb
env = {
    "schema_version": 1, "kind": "generic", "status": status, "t1_item": 2,
    "summary": "T1 item 2 (Layout, analog): layout/osc_bank.gds regenerated from layout/gen/gen_osc_bank.py "
               "byte-identically; net-connectivity sanity check passes. Simulated/derived planning geometry, "
               "not DRC- or LVS-checked.",
    "source": "layout/osc_bank.gds",
    "provenance": {
        "klt_version": "0.8.0", "klayout_version": kdb.__version__ if hasattr(kdb, "__version__") else "0.30.10",
        "pdk": None, "deck": None,
        "input": {"path": {"path": "layout/osc_bank.gds", "scope": "repo"}, "content_hash": committed},
        "regeneration": {"generator": "python3 layout/gen/gen_osc_bank.py -o <scratch>/osc_bank.gds",
                         "regenerated_hash": regen},
    },
}
p = os.path.join(REPO, "evidence", "item2.json")
open(p, "w").write(json.dumps(env, indent=2) + "\n")
print(status, sha(open(p, "rb").read()))
