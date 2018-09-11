﻿import click
import os

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


cli = CLIClass(context_settings=Config.CONTEXT_SETTINGS, help="Codechef cli")