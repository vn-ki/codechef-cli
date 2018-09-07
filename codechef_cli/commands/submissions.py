import click
import logging


logger = logging.Logger(__name__)


@click.group()
def cli():
    """Submit your solution to a problem and view it's status."""
    pass


@cli.command()
@click.option(
    '--problem-code', '-pc', metavar='ID',
    help="The problem code of the problem you are submitting."
)
@click.option(
    '--contest-code', '-cc', metavar='ID',
    help="The contest code of the problem you are submitting."
)
def add(problem_code, contest_code):
    """Add a submission."""


@cli.command()
def showall():
    """Show all submissions."""


@cli.command()
@click.argument('uid', required=False)
def status(uid):
    """Show the status of the last submission."""
