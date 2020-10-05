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

    with open(GROUPS_FILE, 'r') as file:
        groups = json.load(file)

    counter = 0
    for group in groups:
        if group['name'] == user_group:
            await get_timetable(user_group)
            counter += 1
        else:
            pass

    return counter > 0


async def get_group_api_id(group_name):
    with open(GROUPS_FILE, 'r') as file:
        groups = json.load(file)

    for group in groups:
        if group['name'] == group_name:
            group_id = group['id']
            return group_id


async def get_timetable(group_name):
    group_id_int = await get_group_api_id(group_name)
    group_id = str(group_id_int)

    timetable_url = f'{DOMAIN}timetable/{group_id}'
    response = requests.get(timetable_url)
    timetable = response.json()

    
    with open(PATH_TO_TT_FILES + group_name + '.json', 'w+') as file:
        json.dump(timetable, file)
    return True


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
    is_even_url = f'{DOMAIN}/CurrentWeek/'
    response = requests.get(is_even_url)
    week_status = response.json()

    return week_status['week'] != 1


async def show_timetable_for_today(user_id, group_name):
    SUBJECT_TYPE = {1: 'Лекция', 2: 'Лабораторная работа', 3: 'Практика'}
    SUPGROUP_NUM = {0: '*', 1: '1', 2: '2'}

    current_day_info = await get_current_day_info()
    current_day_int, current_day_name = current_day_info
    is_week_even = await check_week_status()
    
    message = ''

    weekend_text = 'Сегодня выходной, можете смело отдыхать!'

    with open(PATH_TO_TT_FILES + group_name + '.json', 'r') as file:
        time_table_all = json.load(file)

    message += f'📅 <b>Сегодня:</b> {current_day_name}\n'

    if is_week_even:
        message += f'🗓 <b>Неделя:</b> 2 / чётная\n'
        time_table = time_table_all[0]['even_week']
    else:
        message += f'🗓 <b>Неделя:</b> 1 / нечётная\n'
        time_table = time_table_all[0]['odd_week']

    if current_day_int == 6:
        await bot.send_message(chat_id=user_id, text=weekend_text)

    for lesson in time_table[current_day_int]['lessons']:
        message += f'\n🕙 {lesson["time"]}'
        for subgroup in lesson['subgroups']:
            message += f'\n📚 <b>{subgroup["name"]}</b> '
            message += SUBJECT_TYPE[subgroup['type']]
            message += f'\n👤 {subgroup["teacher"]}'
            message += f'\n🏫 <b>Где</b>: {subgroup["place"]}'
            message += f'\n👥 <b>Подгруппа:</b> {SUPGROUP_NUM[subgroup["num"]]}'
            message += '\n'

    await bot.send_message(chat_id=user_id, text=message, reply_markup=main_menu)
