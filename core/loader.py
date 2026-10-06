import importlib.util
import sys
from pathlib import Path


def load_plugins(plugin_dir):
    plugin_dir = Path(plugin_dir).resolve()
    if not plugin_dir.is_dir():
        return []

    root = str(plugin_dir.parent)
    if root not in sys.path:
        sys.path.insert(0, root)

    loaded = []
    for entry in sorted(plugin_dir.iterdir()):
        if entry.name.startswith(("_", ".")):
            continue
        if entry.is_file() and entry.suffix == ".py":
            mod = _load(entry, f"plugins.{entry.stem}")
        elif entry.is_dir() and (entry / "__init__.py").is_file():
            mod = _load(entry / "__init__.py", f"plugins.{entry.name}")
        else:
            continue
        if mod is not None:
            loaded.append(mod)
    return loaded


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"[loader] {name}: {e}", file=sys.stderr)
        return None
    return module
