import requests
import json
from config import GROUPS_FILE


def get_groups():
    groups_url = 'https://timetable.mysibsau.ru/groups/?format=json'

    response = requests.get(groups_url)
    groups = response.json()

    try:
        with open(GROUPS_FILE, 'w+') as file:
            json.dump(groups, file)
        success_result = f'Группы записаны в {GROUPS_FILE}.json!'
        return success_result
    except:
        fail_text = 'При записи данных произошла ошибка...'
        return fail_text


if __name__ == '__main__':
    print(get_groups())