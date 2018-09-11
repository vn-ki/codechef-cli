import codechef_cli.api.helpers as helpers
import logging

logging.basicConfig()
logger = logging.getLogger("codechef_cli")
logger.setLevel(logging.DEBUG)


def test_helpers():
    helpers.get_data("contests")


test_helpers()
