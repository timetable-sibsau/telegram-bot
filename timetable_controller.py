import json
from os.path import isfile
from datetime import datetime
from main import bot

import requests

from main import db, User
from keyboards import main_menu
from config import GROUPS_FILE, PATH_TO_TT_FILES, DOMAIN


async def does_group_exist(user_id):
    user = db.search(User.id == user_id)
    user_group = user[0]['group']
    # print(user_group)

    with open(GROUPS_FILE, 'r') as file:
        groups = json.load(file)

    counter = 0
    for group in groups:
        if group['name'] == user_group:
            # print(group)
            await get_timetable(user_group)
            counter += 1
        else:
            pass

    if counter > 0:
        return True
    else:
        return False


async def get_group_api_id(group_name):
    with open(GROUPS_FILE, 'r') as file:
        groups = json.load(file)

    for group in groups:
        if group['name'] == group_name:
            group_id = group['id']
            return group_id
        else:
            pass


async def get_timetable(group_name):
    group_id_int = await get_group_api_id(group_name)
    group_id = str(group_id_int)

    timetable_url = DOMAIN + 'timetable/' + group_id + '?format=json'
    response = requests.get(timetable_url)
    timetable = response.json()

    one = 1
    if one > 0:
        with open(PATH_TO_TT_FILES + group_name + '.json', 'w+') as file:
            json.dump(timetable, file)
        return True
    else:
        return False


async def does_timetable_exist(user_id):
    user = db.search(User.id == user_id)
    user_group = user[0]['group']

    try:
        isfile(PATH_TO_TT_FILES + user_group + '.json')
        return True
    except:
        """result = await get_timetable(user_group)
        if result:
            return True
        else:
            return False"""
        return False


async def get_current_day_info():
    week_day_int = datetime.now().weekday()

    week_days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Выходной'
    }

    week_day_info = [week_day_int, week_days[week_day_int]]
    return week_day_info


async def check_week_status():
    is_even_url = DOMAIN + 'CurrentWeek/?format=json'
    response = requests.get(is_even_url)
    week_status = response.json()

    if week_status['week'] == 1:
        return False
    else:
        return True


async def show_timetable_for_today(user_id, group_name):
    current_day_info = await get_current_day_info()
    current_day_int = int(current_day_info[0])
    current_day_name = current_day_info[1]
    is_week_even = await check_week_status()
    super_text = []

    weekend_text = 'Сегодня выходной, можете смело отдыхать!'

    with open(PATH_TO_TT_FILES + group_name + '.json', 'r') as file:
        time_table_all = json.load(file)

    # time_table = time_table_all[0]

    super_text.append(f'📅 <b>Сегодня:</b> {current_day_name}\n')

    if is_week_even:
        super_text.append(f'🗓 <b>Неделя:</b> 2 / чётная\n')
        time_table = time_table_all[0]['even_week']
    else:
        super_text.append(f'🗓 <b>Неделя:</b> 1 / нечётная\n')
        time_table = time_table_all[0]['odd_week']

    if current_day_int != 6:
        for lesson in time_table[current_day_int]['lessons']:
            super_text.append('\n🕙 ')
            super_text.append(lesson['time'])
            for subgroup in lesson['subgroups']:
                super_text.append('\n📚 <b>')
                super_text.append(subgroup['name'])
                super_text.append('</b> ')
                if subgroup['type'] == 1:
                    super_text.append('Лекция')
                elif subgroup['type'] == 2:
                    super_text.append('Лабораторная работа')
                else:
                    super_text.append('Практика')
                super_text.append('\n👤 ')
                super_text.append(subgroup['teacher'])
                super_text.append('\n🏫 <b>Где</b>: ')
                super_text.append(subgroup['place'])
                super_text.append('\n👥 <b>Подгруппа:</b> ')
                if subgroup['num'] == 0:
                    super_text.append('*')
                elif subgroup['num'] == 1:
                    super_text.append('1')
                else:
                    super_text.append('2')
                super_text.append('\n')
        await bot.send_message(chat_id=user_id, text=''.join(super_text), reply_markup=main_menu)
    else:
        await bot.send_message(weekend_text)
