#!/usr/bin/env bash
# Refuse to proceed unless the PDK revision and tool versions match the pins
# in sim/pdk.json and sim/toolchain.json. Prints the resolved PDK root on
# stdout's last line (PDK_ROOT=...) so callers can reuse it.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -I - "$HERE" <<'PY'
import json, os, re, subprocess, sys
here = sys.argv[1]
pdk = json.load(open(os.path.join(here, "pdk.json")))
tc = json.load(open(os.path.join(here, "toolchain.json")))
errs = []

root = os.path.realpath(os.path.expanduser(
    os.environ.get(pdk["root_override_env"], pdk["default_root"])))
if not os.path.isdir(root):
    errs.append(f"PDK root not found: {root} (set {pdk['root_override_env']})")
else:
    try:
        src = open(os.path.join(root, "SOURCES")).read()
        m = re.search(r"open_pdks\s+([0-9a-f]{40})", src)
        got = m.group(1) if m else None
        if got != pdk["open_pdks"]:
            errs.append(f"open_pdks revision {got} != pinned {pdk['open_pdks']}")
    except OSError as e:
        errs.append(f"cannot read PDK SOURCES: {e}")
    for key in ("model_lib", "cell_spice", "liberty_tt"):
        if not os.path.isfile(os.path.join(root, pdk[key])):
            errs.append(f"missing PDK file ({key}): {os.path.join(root, pdk[key])}")

for name, t in tc["tools"].items():
    try:
        out = subprocess.run(t["cmd"], capture_output=True, text=True, timeout=30)
        text = out.stdout + out.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        errs.append(f"{name}: cannot run {t['cmd'][0]}: {e}")
        continue
    m = re.search(t["regex"], text)
    got = m.group(1) if m else None
    if got != t["expect"]:
        errs.append(f"{name}: version {got} != pinned {t['expect']}")

x = tc["xschem"]
try:
    out = subprocess.run(["dpkg-query", "-W", "-f=${Version}", x["dpkg_package"]],
                         capture_output=True, text=True, timeout=30)
    if out.stdout != x["expect"]:
        errs.append(f"xschem: package version {out.stdout or None} != pinned {x['expect']}")
except (OSError, subprocess.TimeoutExpired) as e:
    errs.append(f"xschem: dpkg-query failed: {e}")

if errs:
    for e in errs:
        print(f"check_env: FAIL: {e}", file=sys.stderr)
    sys.exit(1)
print("check_env: OK")
print(f"PDK_ROOT={root}")
PY
