import click
import sys
import os

import logging

from codechef_cli.config import Config
from codechef_cli.__version__ import __version__

echo = click.echo


@click.group(context_settings=Config.CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """Codechef CLI

    Use codechef from your terminal
    """
    pass
