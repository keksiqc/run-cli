import shlex
import sys
import threading
import time


class Listener:
    def __init__(self, script: str, func: (...)):
        self.func = func
        self.script = script
        self.input = sys.stdin

        self.__commands__ = {"exit": self.exit, "rs": self.restart}

    def exit(self):
        self.console.terminate()
        sys.exit(0)

    def restart(self):
        self.console.terminate()
        self.start()

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
            except Exception:
                pass

    def start(self):
        self.console = self.func(self.script)
        thread = threading.Thread(target=self.listen)
        thread.start()
        thread.join()
