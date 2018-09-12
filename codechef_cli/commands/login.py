import click
import logging

from codechef_cli.api.oauth import CodechefOauth
from codechef_cli.data import Data
from codechef_cli.config import Config

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    '--force', default=False, is_flag=True,
    help="login even if tokens exist"
)
def cli(force):
    """Start the login process, receive tokens and store them"""
    if 'tokens' not in Data.keys() or force:
        global_config = Config['global']
        ccoauth = CodechefOauth(
            global_config['client_id'], global_config['client_secret'])
        ccoauth.start_oauth_flow()
        # if everything went well, our tokens should be in ccoauth.tokens
        Data['tokens'] = ccoauth.tokens
        Data.write()
        print("You're successfully logged in.")
    else:
        print("You're already logged in. Try running with --force")
