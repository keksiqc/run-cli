import os
import shlex
import signal
import sys
from threading import Thread

import yaml
from run_scripts import __version__
from run_scripts.command import Command
from run_scripts.style import style


class Listener:
    def __init__(self, script: str):
        self.script = script
        self.input = sys.stdin
        self.output = sys.stdout

        self.__commands__ = {"exit": self.exit, "rs": self.restart}

    def get_style(self, name: str):
        return style.get(name, "")

    def line(self, text: str, style: str = ""):
        message = self.get_style(style) + text + self.get_style("reset") + "\n"
        self.output.write(message)

    def exit(self):
        sys.exit(0)

    def restart(self):
        self.run_loop_script(self.script)

    def run_loop_script(self, script: str | list):
        if type(script) is str:
            self.line(f"[run] " + __version__, style="yellow")
            self.line(f"[run] to restart at any time, enter `rs`", style="yellow")
            self.line(f"[run] to exit, enter `exit`", style="yellow")
            self.line(f"[run] running `{script}`", style="green")
            os.system(script)
        else:
            self.line(f"[run] " + __version__, style="yellow")
            self.line(f"[run] to restart at any time, enter `rs`", style="yellow")
            self.line(f"[run] to exit, enter `exit`", style="yellow")
            for cmd in script:
                self.line(f"[run] running `{cmd}`", style="green")
                os.system(cmd)

    def get_arguments(self):
        return shlex.split(self.input.readline().replace("\n", ""))

    def invoke_command(self, command: str):
        cmd = self.__commands__.get(command, None)

        if cmd is None:
            return

        cmd()

    def listen(self):
        while True:
            try:
                input = self.get_arguments()
                self.invoke_command(input[0])
            except:
                pass

    def start(self):
        thread = Thread(None, target=self.listen, daemon=True)
        thread.start()
        self.run_loop_script(self.script)


class RunCommand(Command):
    def get_runfile(self) -> dict | None:
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.startswith(("runfile", "run")) and file.endswith((".yml", ".yaml")):
                with open(os.path.join(cwd, file), "r") as f:
                    return yaml.safe_load(f)

    def get_script(self, runfile, script):
        try:
            return runfile["scripts"][script]
        except Exception:
            self.line(f"Script `{script}` not found in runfile", style="red")
            return

    def run_script(self, script: str | list):
        if type(script) is str:
            self.line("$ " + script, style="gray")
            os.system(script)
        else:
            for cmd in script:
                self.line("$ " + cmd, style="gray")
                os.system(cmd)

    def handle(self):
        runfile = self.get_runfile()
        script = self.get_script(runfile, self.argument("script"))

        if script:
            if self.option("loop"):
                listener = Listener(script)
                listener.start()
            else:
                self.run_script(script)
