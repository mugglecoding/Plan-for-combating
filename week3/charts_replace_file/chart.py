__author__ = 'arnoutaertgeerts'


from .core import to_series, to_json_files, show_plot, set_display


class Chart():
    def __init__(self, inline, html, path, show):
        self.inline = inline
        self.html = html
        self.path = path
        self.show_property = show

    def plot(self, *args, **kwargs):
        if len(args) == 2:
            self._plot_single(*args, **kwargs)
        else:
            self._plot_multi(*args, **kwargs)

    def _plot_multi(self, series, display):
        series = to_series(series)
        series = set_display(series, display)

        to_json_files(series, self.path)

    def _plot_single(self, data, name, display):
        series = to_series(dict(data=data, name=name))
        series = set_display(series, display)

        to_json_files(series, self.path, )

    def show(self):
        return show_plot(self.inline, self.html, self.show_property, async=self.path)