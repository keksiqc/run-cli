import sys

from run_scripts.style import style


class Command:
    def __init__(self, *args, **kwargs):
        self.name = args[0]

        self.input = sys.stdin
        self.output = sys.stdout
        self._arguments = kwargs.get("arguments", {})
        self._options = kwargs.get("options", {})

    def argument(self, name: str):
        return self._arguments.get(name, None)

    def option(self, name: str):
        return self._options.get(name, None)

    def get_style(self, name: str):
        return style.get(name, "")

    def write(self, text: str, style: str = ""):
        message = self.get_style(style) + text + self.get_style("reset")
        self.output.write(message)

    def line(self, text: str, style: str = ""):
        message = self.get_style(style) + text + self.get_style("reset") + "\n"
        self.output.write(message)
