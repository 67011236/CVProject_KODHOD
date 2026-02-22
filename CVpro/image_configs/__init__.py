# ============================================================================
#                        IMAGE CONFIGS — AUTO-DISCOVERY
# ============================================================================
# Each image has its own config file named  img<stem>.py
# e.g.  img1.py  ←→  1.jpg,   img3.py  ←→  3.jpg
#
# To add config for a new image, just create a new imgX.py file — no other
# file needs to be edited.  This keeps team members from conflicting on git.
# ============================================================================

import os
import importlib

_DEFAULT = {
    # None  →  show all extraction colors except 'black'
    'extract_colors': None,
    # None  →  show all filter colors except 'blue'
    'filter_colors': None,
    'extract_descriptions': {},
    'filter_descriptions': {},
}

_REGISTRY: dict = {}

# ── Auto-discover every  imgX.py  in this package ───────────────────────────
_pkg_dir = os.path.dirname(__file__)
for _fname in sorted(os.listdir(_pkg_dir)):
    if _fname.startswith('img') and _fname.endswith('.py'):
        _key = _fname[3:-3]          # 'img1.py'  →  '1'
        _mod = importlib.import_module(f'image_configs.{_fname[:-3]}')
        if hasattr(_mod, 'CONFIG'):
            _REGISTRY[_key] = _mod.CONFIG


def get_image_config(image_path: str) -> dict:
    """Return the config dict for the given image file path.

    Args:
        image_path: full or relative path to the image file.

    Returns:
        Config dict with keys:
          extract_colors       – list[str] | None
          filter_colors        – list[str] | None
          extract_descriptions – dict[color_key, (title, body)]
          filter_descriptions  – dict[filter_key, (title, body)]
    """
    stem = os.path.splitext(os.path.basename(image_path))[0]  # '1.jpg' → '1'
    return _REGISTRY.get(stem, _DEFAULT)
