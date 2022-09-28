import os

from run_scripts.command import Command


class InitCommand(Command):
    def check_for_runfile(self):
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.startswith(("runfile", "run")) and file.endswith((".yml", ".yaml")):
                return file
        else:
            return False

    def create_runfile(self):
        if self.option("short"):
            file = "run.yml"
        else:
            file = "runfile.yml"

        with open(file, "w") as f:
            f.write("scripts:\n")

        return file

    def handle(self):
        cwd = os.getcwd()
        file_name = self.check_for_runfile()
        if file_name:
            self.line(
                f"Runfile already exists at {os.path.join(cwd, file_name)}", style="red"
            )
        else:
            file_name = self.create_runfile()
            self.line(
                f"Runfile created at {os.path.join(cwd, file_name)}", style="green"
            )
