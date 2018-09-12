import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Information about contests."""
    pass


@cli.command()
@click.option(
    '--contest-code', '-cc', metavar='CODE',
    help="The problem code of the problem you are submitting."
)
@click.option(
    '--filter',
    type=click.Choice(['ongoing', 'past', 'upcoming']),
    help="The contest code of the problem you are submitting."
)
def show(problem_code, contest_code):
    """Show all contests or a specific contest."""


@cli.command()
@click.option(
    '--problem-code', '-pc', metavar='ID',
    help="The problem code of the problem you are submitting."
)
@click.option(
    '--contest-code', '-cc', metavar='ID',
    help="The contest code of the problem you are submitting."
)
def problems(problem_code, contest_code):
    """See problems in a contest."""
