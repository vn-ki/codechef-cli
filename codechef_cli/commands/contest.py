import click
import logging

from codechef_cli import api, tui, util
from codechef_cli.data import Data

logger = logging.Logger(__name__)


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
    default='present',
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
        # contests = util.format_search_results(contests, keys=['code', 'name', 'startDate', 'endDate'])
        contests = util.select_one(contests,
                                   keys_colors=[['code', {'fg': 'yellow', 'bold': True}],
                                                ['name', {'fg': 'blue', 'bold': True}],
                                                'startDate', 'endDate'])
        Data['_last_accesed_contest'] = contests
        tui.draw_contest_page(api.get_contest(contests['code']))

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
    if not contest_code:
        contest = Data['_last_accesed_contest']
        tui.draw_contest_page(api.get_contest(contest['code']))
