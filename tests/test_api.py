import codechef_cli.api.helpers as helpers
from codechef_cli import api
import json

from unittest.mock import patch


def test_helpers():
    # helpers.get_data("contests")
    pass


def test_get_contest():
    with patch('codechef_cli.api.helpers.call_api') as mock_get_data:
        mock_get_data.return_value = json.load(
            open('tests/mocks/contest_jan17.json'))
        contest = api.get_contest('jan17')

    assert contest.contest_code == 'JAN17'
    assert len(contest.problem_codes) == 10
