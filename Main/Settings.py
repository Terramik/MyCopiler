import json
from pathlib import Path


__all__ = ('settings_create', 'settings_load')


base_settings = {
    'compiler': 'gcc'
}


relpath = Path(__file__).parent


def settings_create():
    with open(relpath / '../Settings.json', 'w') as f:
        json.dump(base_settings, f, indent=4)


def settings_load() -> dict | None:
    with open(relpath / '../Settings.json', 'r') as f:
        res = json.load(f)
        if isinstance(res, dict) and \
            set(res) == set(base_settings):
            return res
    return None



#settings_create()






