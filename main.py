import json
import requests
import datetime
from pprint import pprint


class StackoverflowQuestion:
    """Class for requests to stackoverflow with initialized questions dictionary"""
    def __init__(self):
        self.all_questions = {}

    def get_questions(self, interest_tag=None, day_count=2):
        """
        Function gets questions from stackoverflow for the last day_count days
        (for example day_count=2 and date is 15/03/2023, so min creation date will be 13/03/2023 -
        time is not in calculation).
        Also, you may add interesting tag as parameter (for example - 'python').
        Function returns list of questions, consisting of question title, creation date and question tags.
        Return list is sorted on creation date attribute.

        :param interest_tag:
        :param day_count:
        :return :
        """
        request_date = datetime.date.today()
        request_date = datetime.datetime.strptime(
            str(request_date - datetime.timedelta(days=day_count)) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        request_date = int(request_date.timestamp())
        if interest_tag:
            url = 'https://api.stackexchange.com/2.3/questions?tagged=' \
                  + interest_tag + '&fromdate=' + str(request_date) + '&site=stackoverflow'
            response = requests.get(url)
        else:
            url = 'https://api.stackexchange.com/2.3/questions?fromdate=' \
                                    + str(request_date) + '&site=stackoverflow'
            response = requests.get(url)
        self.all_questions = json.loads(response.text)
        return sorted([(elem['title'],
                        datetime.datetime.fromtimestamp(elem['creation_date']).strftime("%d.%m.%Y %H:%M:%S"),
                        elem['tags']) for elem in self.all_questions['items']], key=lambda x: x[1])


if __name__ == '__main__':
    question = StackoverflowQuestion()
    print('Questions in stackoverflow are:')
    pprint(question.get_questions('python', 2))
