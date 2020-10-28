import requests
import json
from config import GROUPS_FILE, DOMAIN, HEADERS


def get_groups():
    groups_url = DOMAIN + 'groups/?format=json'

    response = requests.get(groups_url, headers=HEADERS)
    groups = response.json()

    try:
        with open(GROUPS_FILE, 'w+') as file:
            json.dump(groups, file)
        success_result = f'Группы записаны успешно в: {GROUPS_FILE}'
        return success_result
    except:
        fail_text = 'При записи данных произошла ошибка...'
        return fail_text


if __name__ == '__main__':
    print(get_groups())

