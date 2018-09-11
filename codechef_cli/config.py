import click
import os
import errno
import json

APP_NAME = 'codechef'
APP_DIR = click.get_app_dir(APP_NAME)
DEFAULT_CONFIG = {
    'global': {
        'client_id': "a5a5697c8f2bfcbc816635b0e6c05b83",
        'client_secret': "1247a2aa0a2f37f00003a3fe9d15a2d3"
    },
}


class _Config():
    FILE = os.path.join(APP_DIR, 'config.json')
    DEFAULT_VALUES = DEFAULT_CONFIG

    def __init__(self):
        try:
            os.makedirs(APP_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(self.FILE):
            self._write_default_config()
            self._CONFIG = self.DEFAULT_VALUES
        else:
            self._CONFIG = self._read_config()

            # TODO:@vn-ki: we don't need this, right?
            # def update(gkey):
            # for key, val in self.DEFAULT_VALUES[gkey].items():
            # if key not in self._CONFIG[gkey].keys():
            # self._CONFIG[gkey][key] = val

            # for key in ['dl', 'watch']:
            # update(key)
            # self.write()

    @property
    def CONTEXT_SETTINGS(self):
        return dict(
            default_map=self._CONFIG
        )

    def __getitem__(self, attr):
        return self._CONFIG[attr]

    def __setitem__(self, attr, value):
        self._CONFIG[attr] = value

    def keys(self):
        return self._CONFIG.keys()

    def write(self):
        self._write_config(self._CONFIG)

    def _write_config(self, config_dict):
        with open(self.FILE, 'w') as configfile:
            json.dump(config_dict, configfile, indent=4, sort_keys=True)

    def _read_config(self):
        with open(self.FILE, 'r') as configfile:
            conf = json.load(configfile)
        return conf

    def _write_default_config(self):
        self._write_config(self.DEFAULT_VALUES)


Config = _Config()
