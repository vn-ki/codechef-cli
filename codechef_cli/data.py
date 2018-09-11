import os

from codechef.config import _Config, APP_DIR


class _Data(_Config):
    FILE = os.path.join(APP_DIR, 'persistent_data.json')
    DEFAULT_VALUES = {}

    def __setitem__(self, attr, value):
        self._CONFIG[attr] = value
        self.write()
