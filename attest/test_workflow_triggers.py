#!/usr/bin/env python3
"""Merge-queue trigger guard: every workflow declares `merge_group` (issue #254).

Run: python3 -I attest/test_workflow_triggers.py

Standard library only -- no forge access, no YAML dependency, nothing
simulated. This module reads the bytes of the files under
`.github/workflows/` and nothing else.

Why this exists
---------------
The chip merge-queue rollout (2AMLogic/2am#7605) fires the repo's required
checks a second time, on `merge_group` events, when a pull request enters the
queue. A workflow that does not declare `merge_group:` never runs there, so
its required context goes green-by-absence in the queue and the queue can
never start (the operator's `repo-ruleset-policy.py --merge-queue-repo` refuses
while the trigger is missing). Nothing else in this repo sees the `on:` blocks:
a workflow could silently lose the trigger -- or grow a path/branch filter that
narrows which pull requests its checks cover -- and only a live queue refusal
would surface it, one operator round-trip later.

What it checks
--------------
For every workflow file under `.github/workflows/`:

1. The `on:` block exists and is block-style (`on:` alone on its line). Flow
   style (`on: [push, ...]`) is a clear failure, not a silent pass, so a
   rewrite cannot hide triggers from this scanner.
2. `merge_group` is declared -- bare, with no sub-key filters, so the workflow
   fires for every queued merge group (the sibling adaptation
   sky130-comparator#332 added the same trigger unfiltered).
3. `pull_request` carries no `paths:`/`branches:` filters, locking in the
   trigger-only shape this change ships: a filtered `pull_request` narrows
   which pull requests get the check before the queue ever sees them.

Trigger parsing is a minimal indentation scanner, not a YAML parser: top-level
`on:`, then the deeper-indented block, skipping comment lines. Anything this
scanner cannot understand is a failure, never an assumption.
"""
import glob
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORKFLOW_GLOBS = [
    os.path.join(REPO, ".github", "workflows", "*.yml"),
    os.path.join(REPO, ".github", "workflows", "*.yaml"),
]


class MissingOnError(ValueError):
    """The workflow has no top-level `on:` block."""


class FlowStyleOnError(ValueError):
    """The `on:` block is flow-style, which this scanner refuses to guess at."""


def parse_on_triggers(text):
    """Trigger names declared in a workflow's `on:` block -> {name: sub_keys}.

    `sub_keys` is the list of filter keys indented under the trigger (empty
    for a bare `trigger:` line). Raises MissingOnError when no top-level
    `on:` line exists and FlowStyleOnError when the `on:` line carries an
    inline value (`on: push`, `on: [push]`) instead of opening a block.
    """
    lines = text.splitlines()
    on_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line == "on:":
            on_idx = i
            break
        if line.startswith("on:"):
            # Top-level flow style (`on: push`, `on: [push]`): refuse loudly
            # rather than guessing at triggers this scanner cannot see.
            raise FlowStyleOnError(
                "line %d is %r: `on:` must open a block-style mapping"
                % (i + 1, stripped)
            )
        # Any other top-level key (name:, permissions:, jobs:, ...) or a
        # deeper-indented line of an earlier block: keep scanning.
        continue
    if on_idx is None:
        raise MissingOnError("no top-level `on:` block found")

    triggers = {}
    current = None
    for line in lines[on_idx + 1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            break  # the on: block ended
        if current is not None and indent <= current[1]:
            current = None
        if current is None:
            name = stripped.split(":", 1)[0]
            inline = stripped.split(":", 1)[1].strip()
            if inline:
                raise FlowStyleOnError(
                    "trigger %r uses flow style (%r): filters must be a "
                    "block-style mapping" % (name, stripped)
                )
            current = (name, indent)
            triggers[name] = []
        else:
            triggers[current[0]].append(stripped.split(":", 1)[0])
    return triggers


def check_text(text):
    """Violations (human-readable strings) for one workflow file's content.

    Raises MissingOnError / FlowStyleOnError so an unparseable `on:` block
    fails loudly instead of silently disabling the guard.
    """
    triggers = parse_on_triggers(text)
    violations = []
    if "merge_group" not in triggers:
        violations.append(
            "no `merge_group:` trigger: the workflow never runs when a pull "
            "request enters the merge queue, so its required context is "
            "green-by-absence there"
        )
    elif triggers["merge_group"]:
        violations.append(
            "`merge_group:` must be bare (no %s filter) so every queued "
            "merge group runs the check" % "/".join(triggers["merge_group"])
        )
    if "paths" in triggers.get("pull_request", []) or "branches" in triggers.get(
        "pull_request", []
    ):
        violations.append(
            "`pull_request:` carries a paths/branches filter: the trigger-only "
            "shape this repo ships keeps it firing for every pull request"
        )
    return violations


class TestCurrentWorkflows(unittest.TestCase):
    def test_every_workflow_declares_bare_merge_group(self):
        paths = sorted(set(sum((glob.glob(g) for g in WORKFLOW_GLOBS), [])))
        self.assertTrue(paths, "no workflow files under .github/workflows/")
        for path in paths:
            with self.subTest(workflow=os.path.relpath(path, REPO)):
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
                # A malformed on: block must fail this test too: let
                # MissingOnError / FlowStyleOnError propagate.
                violations = check_text(text)
                self.assertEqual(violations, [], "\n".join(violations))


class TestGuardSelfcases(unittest.TestCase):
    """The guard's own cases, on synthetic workflow texts (cf. #332: the
    selftests grow with the gate, so a blind spot cannot ship unnoticed)."""

    BARE = "name: w\non:\n  push:\n  pull_request:\n  merge_group:\n  workflow_dispatch:\n"

    def test_bare_triggers_pass(self):
        self.assertEqual(check_text(self.BARE), [])

    def test_missing_merge_group_fails(self):
        text = "on:\n  push:\n  pull_request:\n  workflow_dispatch:\n"
        self.assertIn("no `merge_group:` trigger", "\n".join(check_text(text)))

    def test_filtered_merge_group_fails(self):
        text = "on:\n  push:\n  merge_group:\n    branches:\n      - main\n"
        self.assertIn("must be bare", "\n".join(check_text(text)))

    def test_path_filtered_pull_request_fails(self):
        text = "on:\n  pull_request:\n    paths:\n      - 'sim/**'\n  merge_group:\n"
        self.assertIn("paths/branches filter", "\n".join(check_text(text)))

    def test_missing_on_block_is_a_clear_failure(self):
        with self.assertRaises(MissingOnError):
            parse_on_triggers("name: w\njobs: {}\n")

    def test_flow_style_on_is_a_clear_failure(self):
        with self.assertRaises(FlowStyleOnError):
            parse_on_triggers("on: [push, pull_request]\n")

    def test_flow_style_trigger_is_a_clear_failure(self):
        with self.assertRaises(FlowStyleOnError):
            parse_on_triggers("on:\n  pull_request: [opened, synchronize]\n")

    def test_comments_and_top_level_keys_do_not_confuse_the_scanner(self):
        text = (
            "# lead comment\non:\n  # trigger comment\n  push:\n"
            "  merge_group:\npermissions:\n  contents: read\n"
        )
        self.assertEqual(
            parse_on_triggers(text), {"push": [], "merge_group": []}
        )


if __name__ == "__main__":
    unittest.main()
