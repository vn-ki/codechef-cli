import click
import os

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
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']



@click.group(cls=CLIClass, context_settings=Config.CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option(
    '--log-level', '-ll',
    type=click.Choice(['ERROR', 'WARNING', 'INFO', 'DEBUG']),
    default='INFO',
    help="Log Level"
)
def cli(log_level):
    """Codechef CLI"""
    util.setup_logger(log_level)
    util.print_info(__version__)
