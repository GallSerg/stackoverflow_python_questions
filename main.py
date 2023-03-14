import json
import requests
import datetime


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
        Function returns list of questions, consisting of question title and creation date.
        Return list is sorted on creation date attribute.

        :param interest_tag:
        :param day_count:
        :return :
        """
        request_date = datetime.date.today()
        request_date = datetime.datetime.strptime(
            str(request_date - datetime.timedelta(days=day_count)) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        request_date = int(request_date.timestamp())
        page = 1
        has_more = True
        while has_more:
            print("Loading data from page", page)
            if interest_tag:
                url = f'https://api.stackexchange.com/2.3/questions?page={str(page)}&pagesize=100' \
                      f'&tagged={interest_tag}&fromdate={str(request_date)}&site=stackoverflow'
                response = requests.get(url)
            else:
                url = f'https://api.stackexchange.com/2.3/questions?page={str(page)}&pagesize=100' \
                      f'&fromdate={str(request_date)}&site=stackoverflow'
                response = requests.get(url)
            response_text = json.loads(response.text)
            if self.all_questions == {}:
                self.all_questions = response_text
            else:
                self.all_questions['items'].extend(response_text['items'])
            has_more = response_text['has_more']
            page += 1
        print("Load data complete")
        return sorted([(elem['title'],
                        datetime.datetime.fromtimestamp(elem['creation_date']).strftime("%d.%m.%Y %H:%M:%S"))
                       for elem in self.all_questions['items']], key=lambda x: x[1])


if __name__ == '__main__':
    question = StackoverflowQuestion()
    with open("output.txt", 'w', encoding='utf-8') as out:
        [print(f'{i}: {v}', file=out) for i, v in enumerate(question.get_questions('python', 2), 1)]
