import click
import logging
import re
import requests

from codechef_cli.data import Data
from codechef_cli.api.helpers import get_data


logger = logging.getLogger(__name__)


def _update_submit_userdata():
    cookies = click.prompt("enter cookies(single line)")
    user_agent = click.prompt("enter user-agent(single line)")
    Data["submit_userdata"] = {
        "cookies": cookies,
        "user_agent": user_agent
    }


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
    help="The language **id** in which your code is written",
    required=True
)
@click.option(
    '--input-file', '-if', metavar='ID',
    help="The file containing code",
    required=True
)
# @click.option(
# '--contest-code', '-cc', metavar='ID',
# help="The contest code of the problem you are submitting."
# )
def add(problem_code, input_file, language):
    """Add a submission."""
    # TODO:
    """
     - if not Data["submit_userdata"], ask for cookies and UA
     - if not input, take from stdin
     * Currently we'll send program as string only, if input is file,
       just read it into string
     - request.get("submit/{problem_code}") and find form_build_id and form_token
       example: <input type="hidden" name="form_build_id" id="..." value="..."  />
     - request.post("submit/{problem_code}") with
       - form_build_id, form_token, form_id:problem_submission, program, language, problem_code
     - find submission_id from req.url
     - print and store it
    """
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    # read userdata
    if "submit_userdata" not in Data.keys():
        _update_submit_userdata()
    userdata = Data["submit_userdata"]
    cookies = userdata["cookies"]
    user_agent = userdata["user_agent"]

    # fetch tokens
    problem_url = "https://www.codechef.com/submit/{}".format(problem_code)
    session = requests.Session()
    session.headers = {
        "Cookie": cookies,
        "User-Agent": user_agent
    }
    r = session.get(problem_url)
    try:
        form_token = re.search(
            r"name=\"form_token\".*?value=\"(.*?)\"", r.text).group(1)
        form_build_id = re.search(
            r"name=\"form_build_id\".*?value=\"(.*?)\"", r.text).group(1)
        logger.debug("form_token: {}, form_build_id:{}".format(
            form_token, form_build_id))
    # TODO: more robust way to conclude that tokens are expired?
    except AttributeError:
        click.echo("Your tokens are no longer valid. Please enter the new ones.")
        _update_submit_userdata()
        # TODO: run command again
        return

    # send the code
    r = session.post(problem_url, data={
        "form_token": form_token,
        "form_build_id": form_build_id,
        "form_id": "problem_submission",
        "program": "",
        # TODO:create a map of languages and ids
        "language": language,
        "problem_code": problem_code
    }, files={
        "files[sourcefile]": open(input_file, 'r')
    })

    # done
    submission_code = re.search(r"complete/(\d+)", r.url).group(1)
    click.echo(submission_code)


@cli.command()
def showall():
    """Show all submissions."""


@cli.command()
@click.argument('uid', required=False)
def status(uid):
    """Show the status of the last submission."""
    resp = get_data("submissions", uid)
    # TODO:print response in a useful manner
    print(resp)
