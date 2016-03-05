__author__ = 'arnoutaertgeerts'

from string import Template
from .jsonencoder import ChartsJSONEncoder
from .server import url

import os
import json
import shutil
import webbrowser
import re


class MyTemplate(Template):
    delimiter = '$#'
    idpattern = r'[a-z][_a-z0-9]*'


def show_plot(html, saveHTML, show, async=False):
    if show == 'inline':
        from IPython.display import HTML
        return HTML(html)

    elif show == 'tab':
        print('Opening new tab...')
        if async:
            address = url(async)
            webbrowser.open_new_tab(address)
        else:
            webbrowser.open_new_tab('file://' + os.path.realpath(saveHTML))

    elif show == 'window':
        print('Trying to open a window. If this fails we will open a tab...')
        if async:
            address = url(async)
            webbrowser.open_new(address)
        else:
            webbrowser.open_new('file://' + os.path.realpath(saveHTML))

    elif show == 'string':
        return html


def clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def to_json_files(series, path):
    try:
        with open(os.path.join(path, 'keys.json'), "r") as keys_file:
            keys = json.loads(keys_file.read())
    except IOError:
        keys = []

    for k in keys:
        k["display"] = False

    for s in series:
        if s["name"] not in map(lambda x: x["name"], keys):
            keys.append(dict(name=s["name"], display=s["display"], value=s["name"], text=s["name"]))
            with open(os.path.join(path, s["name"] + ".json"), "w") as json_file:
                json_file.write(json.dumps(s, cls=ChartsJSONEncoder))
        else:
            i = find(keys, "name", s["name"])
            keys[i] = dict(name=s["name"], display=s["display"], value=s["name"], text=s["name"])

    with open(os.path.join(path, 'keys.json'), "w") as keys_file:
        keys_file.write(json.dumps(keys))


def find(col, key, value):
    for i, c in enumerate(col):
        if c[key] == value:
            return i


def set_display(series, display):
    if display is True:
        for s in series:
            s['display'] = True

    elif display is False:
        for s in series:
            s['display'] = False

    else:
        for s in series:
            if s['name'] in display:
                s['display'] = True
            else:
                s['display'] = False

    return series


def df_to_series(df):
    """Prepare data from dataframe for plotting with python-highcharts.
    all columns in df are entries in the returned series.
    The returned series is in the format suitable for python-highcharts: list of dicts with:
    data:list of [index, value]-lists.
    name:name of variable.
    """

    import pandas as pd
    import numpy as np

    df = df.where((pd.notnull(df)), None)

    if isinstance(df.index, pd.DatetimeIndex):
        index = df.index.asi8 / (1e6)
    else:
        index = df.index

    series = []
    for col in df:
        series.append(
            dict(name=col,
                 data=np.array([index, df[col].values]).T,
                 display=False)
        )

    return series


def list_to_series(array):
    return dict(
        data=array
    )


def to_series(series, name=False):
    # Dictionary?
    if isinstance(series, dict):
        return [series]

    # List of dictionaries?:
    try:
        if isinstance(series[0], dict):
            return series
    except KeyError:
        pass

    # List?
    try:
        if isinstance(series, list):
            return [dict(data=series, name=name)]
    except KeyError:
        pass

    # Numpy array?
    try:
        import numpy as np
        if isinstance(series, np.ndarray):
            return [dict(data=series, name=name)]
    except ImportError:
        pass

    # pandas DataFrame or series?
    try:
        import pandas as pd
        if isinstance(series, pd.DataFrame):
            return df_to_series(series)
        if isinstance(series, pd.Series):
            return df_to_series(pd.DataFrame(series))
    except ImportError:
        pass

    raise ValueError('Your data is not in the right format!')

def remove_quotes(options):

    options = json.dumps(options)

    ix = [m.start() for m in re.finditer('@#', options)]

    for j, i in enumerate(ix):
        k = i-3*j
        if options[k-1] == '"':
            options = options[:k-1] + options[k+2:]
        else:
            options = options[:k] + options[k+3:]

    return options