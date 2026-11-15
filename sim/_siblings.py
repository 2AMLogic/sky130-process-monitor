"""Load a sibling module from another sim/ subdirectory, by path, once per process.

Every script under sim/ is run as `python3 -I sim/<dir>/<script>.py` (README, CI and the
signoff manifests all do), and `python3 -I` drops the script directory from sys.path, so a
cross-directory sibling cannot be reached with a plain `import`: it must be loaded by path.
The bare names are ambiguous too - gen_requests.py and analyze.py each exist in several sim/
subdirectories - so the module is loaded under the synthetic name `<pkg>_<mod>`, which
collides with no real module and cannot self-reference through a same-named sys.modules
entry the way a bare-name import can (the failure that disqualified issue #175's direction).

One convention, documented here instead of once per site. From a script in sim/<dir>/:

    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    import _siblings  # noqa: E402

    _SENS = _siblings.load("sensitivity", "analyze")

`sim/` itself holds no other top-level .py, so `_siblings` is a unique name and the one
sys.path entry adds no ambiguity. The helper resolves `sim/<pkg>/<mod>.py` against the
CALLER's __file__ (not its own) so a relocated copy - test_analyze_power.py moves one beside
substitute sensitivity modules - tracks its own tree, and memoises the loaded module in
sys.modules keyed on the resolved absolute path, so each file executes once per process yet
two trees stay two distinct modules.
"""
import importlib.util
import os
import sys


def load(pkg, mod):
    """Load sim/<pkg>/<mod>.py relative to the calling module's directory and return it.

    Memoised in sys.modules under `<pkg>_<mod>@<resolved abs path>`: keyed on the path so
    two trees load as two modules, named with the synthetic `<pkg>_<mod>` prefix so the
    key can never collide with a real module's entry.
    """
    caller_dir = os.path.dirname(os.path.abspath(sys._getframe(1).f_globals["__file__"]))
    path = os.path.normpath(os.path.join(caller_dir, "..", pkg, mod + ".py"))
    key = "%s_%s@%s" % (pkg, mod, path)
    module = sys.modules.get(key)
    if module is not None:
        return module
    spec = importlib.util.spec_from_file_location("%s_%s" % (pkg, mod), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module  # registered before exec, so a cycle re-enters, not re-runs
    spec.loader.exec_module(module)
    return module
