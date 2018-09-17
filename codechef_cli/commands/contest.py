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
    if contest_code is None:
        contests = api.get_data('contests', params={
            'fields': 'code, name, startDate, endDate',
            'limit': 50,
            'status': filter,
        })['contestList']
        contests = util.select_one(
            contests,
            keys_colors=[['code', {'fg': 'yellow', 'bold': True}],
                         ['name', {'fg': 'blue', 'bold': True}],
                         'startDate', 'endDate']
        )
        Data['_last_accesed_contest'] = contests
        tui.draw_contest_page(api.get_contest(contests['code']))

    else:
        contest = api.get_data('contests', contest_code)
        tui.draw_contest_page(api.get_contest(contest['code']))


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


@cli.command()
@click.argument('contest_code', required=False)
@click.option(
    '--country', '-c',
    help='Country to which the user belongs, eg. India'
)
@click.option(
    '--institution', '-i',
    help='Institution to which the user belongs, eg. Indian Institute of Technology Indore'
)
def rankings(contest_code, country, institution):
    """Ranklist of a contest. If contest ID not given selects the last accesed contest."""
    if contest_code is None:
        contest_code = Data['_last_accesed_contest']['code']

    ranklist = api.get_data('rankings', contest_code, params={
        'fields': 'rank,username,country,totalScore',
        'country': country,
        'institution': institution,
        'limit': 25,
        'sortBy': 'rank',
        'sortOrder': 'asc',
    })

    ranks = util.tabulate(
        ranklist,
        keys_colors=[['rank', {'fg': 'yellow', 'bold': True}],
                     ['username', {'fg': 'blue', 'bold': True}],
                     'country', 'totalScore'],
        add_num=False,
    )
    click.echo_via_pager(ranks)
