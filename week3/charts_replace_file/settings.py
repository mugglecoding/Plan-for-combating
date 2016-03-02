__author__ = 'Arnout Aertgeerts'
import json


class DefaultDict(dict):
    def __init__(self, **kwargs):
        self.default = kwargs

        super(DefaultDict, self).__init__(kwargs)

    def reset(self):
        self.update(self.default)


default_settings = DefaultDict(type='line', name=False, height=400, save=False, stock=False, show='tab', display=True)
default_options = DefaultDict(width='auto', height=400, scale=2, type='line')


def load_options(path):
    try:
        with open(path, 'r') as json_file:
            return json.loads(json_file.read())
    except IOError:
        print('No options file found. Did you spell the name correctly?')
        return dict()