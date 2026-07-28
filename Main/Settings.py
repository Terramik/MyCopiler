import json


__all__ = ('settings_create', 'settings_load')


base_settings = {
    'compiler': 'gcc'
}


def settings_create():
    with open('../Settings.json', 'w') as f:
        json.dump(base_settings, f, indent=4)


def settings_load() -> dict | None:
    with open('../Settings.json', 'r') as f:
        res = json.load(f)
        if isinstance(res, dict) and \
            set(res) == set(base_settings):
            return res
    return None



#settings_create()






