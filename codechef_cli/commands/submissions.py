import click
import logging

from codechef_cli.data import Data
from codechef_cli.api.helpers import get_data
from codechef_cli.api.submission import submit_solution, _update_submit_userdata
from codechef_cli.exceptions import APIError
import codechef_cli.util as util

logger = logging.getLogger(__name__)


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
    '--language', '-l', metavar='ID',
    help="The language in which your code is written",
    required=True
)
@click.option(
    '--input-file', '-if', metavar='ID',
    type=click.File("rb"),
    help="The file containing code",
    required=True
)
def add(problem_code, input_file, language):
    """Add a submission."""
    if "submit_userdata" not in Data.keys():
        _update_submit_userdata()
    try:
        submission_code = submit_solution(problem_code, input_file, language)
    except APIError:
        click.echo("Your tokens are no longer valid. Please enter the new ones.")
        _update_submit_userdata()
        submission_code = submit_solution(problem_code, input_file, language)
    click.echo('Submission code: '+submission_code)
    click.echo('Use `codechef submissions status` to see the status')


@cli.command()
def showall():
    """Show all submissions."""
    # TODO: print response in a useful manner
    resp = get_data('submissions', params={
        'fields': 'id, date, problemCode, language, contestCode, result, time, memory',
        'limit': 50,
    })
    util.select_one(
        resp,
        keys_colors=[['id', {'fg': 'yellow', 'bold': True}],
                     ['date', {'fg': 'blue', 'bold': True}],
                     'problemCode', 'language', 'contestCode', 'result', 'time', 'memory']
    )


@cli.command()
@click.argument('uid', required=False)
def status(uid):
    """Show the status of the last submission."""
    if not uid:
        uid = Data['_last_submission_code']
    resp = get_data('submissions', uid)
    logging.debug(resp)
    click.secho('Problem Code: ' + resp['problemCode'], fg='green')
    click.secho('Contest Code: ' + resp['contestCode'])
    if resp['result'] == 'CTE':
        click.echo(
            'Result: ' +
            click.style('Compile time Error', bg='red', fg='black')
        )
