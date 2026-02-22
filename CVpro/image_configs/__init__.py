
import os
import importlib

_DEFAULT = {
    'extract_colors': None,
    'filter_colors': None,
    'extract_descriptions': {},
    'filter_descriptions': {},
}

_REGISTRY: dict = {}

_pkg_dir = os.path.dirname(__file__)
for _fname in sorted(os.listdir(_pkg_dir)):
    if _fname.startswith('img') and _fname.endswith('.py'):
        _key = _fname[3:-3]
        _mod = importlib.import_module(f'image_configs.{_fname[:-3]}')
        if hasattr(_mod, 'CONFIG'):
            _REGISTRY[_key] = _mod.CONFIG


def get_image_config(image_path: str) -> dict:
    
    stem = os.path.splitext(os.path.basename(image_path))[0]
    return _REGISTRY.get(stem, _DEFAULT)
