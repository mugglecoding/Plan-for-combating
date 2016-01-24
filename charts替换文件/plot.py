__author__ = 'Arnout Aertgeerts'

from .core import MyTemplate, to_json_files, to_series, clean_dir, set_display, show_plot, make_dir, remove_quotes
from .jsonencoder import ChartsJSONEncoder
from .chart import Chart
from .server import address
from .settings import default_settings, load_options, default_options

import os
import json

package_directory = os.path.dirname(os.path.abspath(__file__))

TABDEPS = """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css"/>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
"""


def line(*args, **kwargs):
    return plot(*args, type='line', **kwargs)


def area(*args, **kwargs):
    return plot(*args, type='area', **kwargs)


def spline(*args, **kwargs):
    return plot(*args, type='spline', **kwargs)


def pie(*args, **kwargs):
    return plot(*args, type='pie', **kwargs)


def stock(*args, **kwargs):
    return plot(*args, stock=True, **kwargs)


def plot(series, options=dict(), **kwargs):
    """
    Make a highchart plot with all data embedded in the HTML
    :param type: Type of the chart (will overwrite options['chart']['type'] if specified).
    :param series: The necessary data, can be a list of dictionaries or a dataframe
    :param options: Options for the chart. This can one of the following:
        - A Dictionary
        - The path to a json file
        - A json string
    :param height: Chart height
    :param save: Specify a filename to save the HTML file if wanted.
    :param stock: Set to False to use Highcharts instead of highstock
    :param show: Determines how the chart is shown. Can be one of the following options:
        - 'tab': Show the chart in a new tab of the default browser
        - 'window': Show the chart in a new window of the default browser
        - 'inline': Show the chart inline (only works in IPython notebook)
    :param display: A list containing the keys of the variables you want to show initially in the plot
    :return: The chart to display
    """

    # Check if options is a json string or file
    if isinstance(options, str):
        if '.json' in options:
            options = load_options(options)
        else:
            try:
                options = json.loads(options)
            except ValueError:
                raise ValueError('Your options string is not valid JSON!')

    chart_settings = default_settings.copy()
    chart_options = default_options.copy()

    chart_settings.update(kwargs)
    chart_options.update(options)

    keys = chart_settings.keys()

    for key in keys:
        if key not in ['options', 'name', 'display', 'save', 'show', 'height', 'type', 'stock', 'width']:
            raise AttributeError(key + ' is not a valid option!')

    options = chart_options
    name = chart_settings['name']
    display = chart_settings['display']
    save = chart_settings['save']
    show = chart_settings['show']
    type = chart_settings['type']
    stock = chart_settings['stock']

    try:
        if options['chart']:
            options['chart'].update(dict(type=type))
    except KeyError:
        options['chart'] = dict(type=type)

    try:
        if not options['height']:
            options['chart'].update(dict(type=type))
    except KeyError:
        options['chart'] = dict(type=type)

    # Convert to a legitimate series object
    series = to_series(series, name)

    # Set the display option
    series = set_display(series, display)

    # Get the save extension
    if save:
        extension = os.path.splitext(save)[1]
    else:
        extension = False

    saveSVG = False
    saveHTML = False

    if extension == '.svg':
        saveSVG = save
    if show != 'inline':
        saveHTML = 'index.html'
    if extension == '.html':
        saveHTML = save

    if 'settingsFile' in options:
        settings_file = options['settingsFile'][:-5]
    else:
        settings_file = 'settings'

    with open(os.path.join(package_directory, "index.html"), "r") as html:
        html = MyTemplate(html.read()).substitute(
            path=package_directory,
            series=json.dumps(series, cls=ChartsJSONEncoder),
            options=remove_quotes(options),
            highstock=json.dumps(stock),
            url=json.dumps(address),
            save=json.dumps(saveSVG),
            settingsFile=json.dumps(settings_file)
        )

    if saveHTML:
        with open(saveHTML, "w") as text_file:
            text_file.write(html + TABDEPS)

    return show_plot(html, saveHTML, show)


def plotasync(
        series=None, options=dict(), type='line',
        height=400, save="temp", stock=False, show='tab', display=False, purge=False, live=False):
    """
    :param type: Type of the chart. Can be line, area, spline, pie, bar, ...
    :param display: Set to true to display all, False to display none or an array of names for a specific selection
    :param purge: Set to true to clean the directory
    :param live: Set to true to keep the chart in sync with data in the directory. Currently only works for show='tab'
    :param series: The series object which contains the data. If this is not specified, the plot will look for json
                   files in the save directory.
    :param options: The chart display options
    :param height: Height of the chart
    :param save: Name of the directory to store the data
    :param stock: Set to true to use highstock
    :param show: Determines how the chart is shown. Can be one of the following options:
        - 'tab': Show the chart in a new tab of the default browser
        - 'window': Show the chart in a new window of the default browser
        - 'inline': Show the chart inline (only works in IPython notebook)
    :return: A chart object
    """

    try:
        if not options['chart']:
            options['chart'] = dict(type=type)
    except KeyError:
        options['chart'] = dict(type=type)

    if 'height' not in options:
        options['height'] = 400

    # Clean the directory
    if purge:
        clean_dir(save)
    else:
        make_dir(save)

    if series is not None:
        # Convert to a legitimate series object
        series = to_series(series)
        series = set_display(series, display)

        # Convert to json files
        to_json_files(series, save)

    if show == 'inline':
        live = False

    with open(os.path.join(package_directory, "index-async.html"), "r") as index:
        read = index.read()

        html = MyTemplate(read).substitute(
            path=json.dumps('/' + save),
            options=json.dumps(options),
            highstock=json.dumps(stock),
            height=str(height) + "px",
            live=json.dumps(live),
            url=json.dumps(address),
            save=json.dumps(False)
        )

        inline = MyTemplate(read).substitute(
            path=json.dumps(save),
            options=json.dumps(options),
            highstock=json.dumps(stock),
            height=str(height) + "px",
            live=json.dumps(live),
            url=json.dumps(address),
            save=json.dumps(False)
        )

    html_path = os.path.join(save, 'index.html')
    with open(html_path, "w") as html_file:
        html_file.write(html + TABDEPS)

    return Chart(inline, html_path, save, show)