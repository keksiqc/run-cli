import os

import click
import yaml

from run_scripts import __version__
from run_scripts.commands.init import InitCommand
from run_scripts.commands.run import RunCommand
from run_scripts.group import RunGroup


@click.group(cls=RunGroup)
def cli():
    pass


@cli.command(name="run", default_command=True)
@click.argument("script")
@click.option("-L", "--loop", "loop", is_flag=True, help="Run the script in loop mode")
def run(script: str, loop: bool):
    _command = RunCommand("run", arguments={"script": script}, options={"loop": loop})
    _command.handle()


@cli.command()
@click.option(
    "-S",
    "--short",
    "short",
    is_flag=True,
    help="Create a run.yml file instead of runfile.yml",
)
def init(short):
    _command = InitCommand("init", options={"short": short})
    _command.handle()
