import click
import logging

<<<<<<< HEAD
logger = logging.getLogger(__name__)
=======
from codechef_cli import api

logger = logging.Logger(__name__)
>>>>>>> b76f1c9... work on compete


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
    type=click.Choice(['past', 'present', 'future']),
    help="The contest code of the problem you are submitting."
)
def show(contest_code, filter):
    """Show all contests or a specific contest."""
    if contest_code == None:
        contests = api.get_data('contests', params={
            'fields': 'code, name, startDate, endDate',
            'limit': 50,
            'status': filter,
        })['contestList']

    else:
        contest = api.get_data('contests', contest_code)


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
