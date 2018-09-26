import click
import importlib
import os
import sys

from codechef_cli import util
from codechef_cli.config import Config
from codechef_cli.__version__ import __version__

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class CLIClass(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        command = importlib.import_module("codechef_cli.commands.{}".format(name))
        return command.cli


@click.group(cls=CLIClass, context_settings=Config.CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option(
    '--log-level', '-ll',
    type=click.Choice(['ERROR', 'WARNING', 'INFO', 'DEBUG']),
    help="Log Level"
)
def cli(log_level):
    """Codechef CLI"""
    util.setup_logger(log_level)
    util.print_info(__version__)


def main():
    try:
        cli()
    except Exception as e:
        if 'DEBUG' in sys.argv:
            raise
        click.echo(click.style('ERROR:', fg='black', bg='red')+' '+click.style(str(e), fg='red'))
