from codechef_cli.api.helpers import get_data
from codechef_cli.api.helper_classes import Contest


def get_contest(contest_code, params=None):
    return Contest(contest_code)
