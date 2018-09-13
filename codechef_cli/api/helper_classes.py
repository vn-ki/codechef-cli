from codechef_cli.api.helpers import get_data
import logging

logger = logging.getLogger(__name__)

class Contest:
    def __init__(self, contest_code):
        self._data = get_data('contests', contest_code)
        self.contest_code = self._data['code']
        self.name = self._data['name']
        self.start_date = self._data['startDate']
        self.end_date = self._data['endDate']
        self.announcements = self._data['announcements']
        self.current_time = self._data['currentTime']  # This is unix time

        self._problems_list = self._data['problemsList']
        self.problem_codes = [prob['problemCode']
                              for prob in self._problems_list]

    def __getitem__(self, index):
        if isinstance(self._problems_list[index], dict):
            self._problems_list[index] = Problem(self._problems_list[index]['problemCode'],
                                                 self.contest_code)
        return self._problems_list[index]

    def is_problem_fetched(self, index):
        return not isinstance(self._problems_list[index], dict)


class Problem:
    def __init__(self, problem_code, contest_code):
        self.problem_code = problem_code
        self.contest_code = contest_code

        self._data = get_data('contests', contest_code,
                              'problems', problem_code)

        self.problem_name = self._data['problemName']
        self.author = self._data['author']
        self.submissions = {
            'success': self._data['successfulSubmissions'],
            'total': self._data['totalSubmissions'],
            'partial': self._data['partialSubmissions'],
        }
        self.tags = self._data['tags']
        self.body = self._data['body']
