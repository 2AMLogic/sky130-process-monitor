#!/usr/bin/env python3
"""Inventory-inputs check for the T1 item-9 attestation inventories (issue #218).

Run: python3 -I attest/test_inventory_inputs.py

Standard library only -- no simulator, no PDK, no `klt`, nothing simulated and nothing
regenerated. This module reads the `attest/item9_*.json` inventories, the bytes of the
files they list, and the repository tree, and nothing else.

Why this exists
---------------
Item 9 is graded per partition, and each partition's envelope stands alone as evidence:
it asserts that a named cold start exited 0 over a set of files the inventory pins by
content hash. That assertion is only as good as the inventory's file list -- an envelope
attesting an outcome whose inputs it does not pin is precisely the defect issue #201
found in the analog partition (fixed by #215) and issue #218 then found again in the
digital partition: `attest/item9_digital.json` attested `make -C verification/readout`,
whose first target runs `sim/check_env.sh`, which loads `sim/pdk.json` and
`sim/toolchain.json` on every invocation -- and none of the three was pinned. An edit to
any of them changed what the attested bench computes without a single hashed byte moving
anywhere, so the `klt signoff` gate stayed green.

The rule this test encodes (issue #218, "Scope decision"): an item-9 inventory pins every
repo file its own declared cold start reads. This test turns a violation into a red CI
run instead of a silently-stale envelope.

What it checks
--------------
1. For each `attest/item9_*.json`: if any inventoried `.sh`/`Makefile`/`.mk` member's
   bytes mention `check_env`, then the check-env script and the JSON files it loads must
   all be inventoried in that same file. Per-partition grading means "the other
   partition pins it" is not a property of this envelope, so the requirement is
   enforced per inventory -- duplication across the two inventories is the accurate
   signal, not redundancy.
2. The rule is not vacuous: at least one inventory actually triggers it (an entrypoint
   reaches `check_env`), and the check-env script is found exactly once in the tree.
   Drop both triggers and this test fails rather than passing silently.
3. Every inventoried path exists at HEAD -- the cheap check that catches a typo'd path
   before an attestation run spends minutes on it.

How the required set is derived
-------------------------------
No hardcoded triple: a hardcoded list that drifts from `check_env.sh` is a weaker guard
than none. The test walks the repository for a file named `check_env.sh` (exactly one
must exist -- ambiguous or absent is a failure), then reads the `json.load` targets out
of its bytes (`os.path.join(here, "pdk.json")` and `os.path.join(here,
"toolchain.json")` today), so a later edit that makes the script load a third pin file
is picked up without touching this test.

Docstring conventions follow `characterization/test_citations.py`.
"""
import json
import os
import re
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INVENTORY_GLOB = "attest/item9_*.json"

# Directory names the tree walk must never descend into: VCS metadata, the Loom
# worktree/scratch area (which contains a second full copy of this repository), virtual
# environments, dependency trees. All hidden directories are pruned, not just `.git`.
PRUNED_DIRS = {".loom", "node_modules", "sim/build", "target", "__pycache__"}

# `json.load(open(os.path.join(here, "pdk.json")))` in sim/check_env.sh: the loaded
# file's name, resolved against the script's own directory (`here`).
_JSON_TARGET = re.compile(r"""json\.load\(open\(os\.path\.join\(here,\s*["']([^"']+)["']\)\)\)""")

# A member whose bytes can reach `check_env`: a shell script, a Makefile, or a make
# include. Decks, requests and Python modules are excluded -- their mentioning the
# string does not mean their cold start runs it.
_TRIGGER_SUFFIXES = (".sh", ".mk", "Makefile")


def _is_trigger_candidate(rel_path):
    """True for an inventoried member whose bytes plausibly invoke check_env."""
    base = os.path.basename(rel_path)
    return base.endswith(".sh") or base.endswith(".mk") or base == "Makefile"


def _read(rel_path):
    """Read a repo-relative file as text. Context-managed so a warning never
    buries a real failure."""
    with open(os.path.join(REPO, rel_path), encoding="utf-8") as fh:
        return fh.read()


def _inventories():
    """The item-9 inventory paths, sorted, repo-relative."""
    attest_dir = os.path.join(REPO, "attest")
    return sorted(
        os.path.join("attest", name)
        for name in os.listdir(attest_dir)
        if name.startswith("item9_") and name.endswith(".json")
    )


def _member_paths(inv_rel):
    """Paths an inventory pins, repo-relative, in listed order. Handles both member
    shapes: bare strings (digital) and {"path": ...} objects (analog)."""
    with open(os.path.join(REPO, inv_rel), encoding="utf-8") as fh:
        inv = json.load(fh)
    out = []
    for m in inv.get("testbenches", []):
        out.append(m["path"] if isinstance(m, dict) else m)
    return out


def _find_check_env_script():
    """The repo-relative path of check_env.sh, found by walking the tree.

    Returns a list so the caller can insist on exactly one: zero means the script
    moved or was deleted (every trigger is now dangling); more than one means the
    walk's pruning failed to keep copies out and the anchor is ambiguous.
    """
    hits = []
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [
            d for d in dirnames if d not in PRUNED_DIRS and not d.startswith(".")
        ]
        if "check_env.sh" in filenames:
            hits.append(os.path.relpath(os.path.join(dirpath, "check_env.sh"), REPO))
    return sorted(hits)


def _required_paths(script_rel):
    """check_env.sh itself plus the JSON files its bytes load, repo-relative.

    The load targets are read out of the script (os.path.join(here, "X") under a
    json.load), so the required set tracks the script instead of duplicating it here.
    """
    required = {script_rel}
    script_dir = os.path.dirname(script_rel)
    for name in _JSON_TARGET.findall(_read(script_rel)):
        required.add(os.path.normpath(os.path.join(script_dir, name)))
    return required


def _missing_required(inv_rel, script_rel):
    """Required paths the inventory fails to pin, sorted."""
    required = _required_paths(script_rel)
    pinned = set(_member_paths(inv_rel))
    return sorted(required - pinned)


class TestRuleEnforced(unittest.TestCase):
    """The scope-decision rule, per inventory: reach check_env -> pin its inputs."""

    def test_each_triggering_inventory_pins_the_check_env_inputs(self):
        scripts = _find_check_env_script()
        self.assertEqual(
            1,
            len(scripts),
            f"expected exactly one check_env.sh in the tree, found {scripts}",
        )
        script = scripts[0]
        for inv in _inventories():
            with self.subTest(inventory=inv):
                members = _member_paths(inv)
                triggers = [
                    m
                    for m in members
                    if _is_trigger_candidate(m) and "check_env" in _read(m)
                ]
                missing = _missing_required(inv, script)
                self.assertEqual(
                    [],
                    missing,
                    f"{inv} reaches check_env (through {triggers}) but does not pin: "
                    f"{missing}. An item-9 inventory pins every repo file its own "
                    "declared cold start reads; without the pin, an edit to the file "
                    "changes what the attested bench computes without moving any "
                    "hashed byte, and the klt signoff gate stays green.",
                )


class TestGuardNotVacuous(unittest.TestCase):
    """The rule must actually bite somewhere, and its anchor must be unambiguous."""

    def test_at_least_one_inventory_triggers_the_rule(self):
        scripts = _find_check_env_script()
        self.assertEqual(1, len(scripts), f"check_env.sh not found uniquely: {scripts}")
        triggered = []
        for inv in _inventories():
            members = _member_paths(inv)
            if any(
                _is_trigger_candidate(m) and "check_env" in _read(m) for m in members
            ):
                triggered.append(inv)
        self.assertTrue(
            triggered,
            "no item-9 inventory reaches check_env, so the inventory-inputs rule "
            "enforces nothing; either the cold starts changed (update this test's "
            "rule) or the inventories lost the entrypoints",
        )

    def test_required_set_covers_the_script_and_its_json_loads(self):
        """Smoke check that the derivation found the real pins, not an empty set."""
        (script,) = _find_check_env_script()
        required = _required_paths(script)
        self.assertIn(script, required)
        self.assertGreaterEqual(
            len(required),
            3,
            f"check_env.sh loads {len(required) - 1} JSON file(s); if the script "
            "stopped loading pins, update this test",
        )
        self.assertEqual(
            {"sim/check_env.sh", "sim/pdk.json", "sim/toolchain.json"},
            required,
            "check_env.sh's derived input set changed; the rule is path-independent "
            "but this smoke check pins the shape",
        )


class TestInventoriedPathsExist(unittest.TestCase):
    """Every inventoried path must exist at HEAD -- the cheap typo check."""

    def test_all_inventoried_paths_exist(self):
        for inv in _inventories():
            for path in _member_paths(inv):
                with self.subTest(inventory=inv, path=path):
                    self.assertTrue(
                        os.path.exists(os.path.join(REPO, path)),
                        f"{inv} pins '{path}', which does not exist at HEAD: a typo "
                        "would make the attestation hash nothing while appearing to "
                        "pin the file",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
