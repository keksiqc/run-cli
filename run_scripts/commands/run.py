import os
import subprocess

import yaml
from run_scripts import __version__
from run_scripts.command import Command
from run_scripts.listener import Listener


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
            self.line("$ " + script, style="dim")
            os.system(script)
        else:
            for cmd in script:
                self.line("$ " + cmd, style="dim")
                os.system(cmd)

    def run_loop_script(self, script: str | list):
        if type(script) is str:
            self.line("[run] " + __version__, style="yellow")
            self.line("[run] to restart at any time, enter `rs`", style="yellow")
            self.line("[run] to exit, enter `exit`", style="yellow")
            self.line(f"[run] running `{script}`", style="green")
            console = subprocess.Popen(
                script, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )
        else:
            console = []
            self.line("[run] " + __version__, style="yellow")
            self.line("[run] to restart at any time, enter `rs`", style="yellow")
            self.line("[run] to exit, enter `exit`", style="yellow")
            for cmd in script:
                self.line(f"[run] running `{cmd}`", style="green")
                _console = subprocess.Popen(
                    script, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
                )
                console.append(_console)

        return console

    def handle(self):
        runfile = self.get_runfile()
        script = self.get_script(runfile, self.argument("script"))

        if script:
            if self.option("loop"):
                listener = Listener(script, self.run_loop_script)
                listener.start()
            else:
                self.run_script(script)
