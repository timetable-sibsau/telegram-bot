import re
import logging

from main import bot, dp, db, User
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from config import ADMIN_ID, BOT_VERSION
from keyboards import main_menu, settings_menu, changing_group_menu


# state
class UserInfo(StatesGroup):
    group = State()


async def notify_admin(dp):
    text = f'<b>Бот запущен!</b>'
    await bot.send_message(chat_id=ADMIN_ID, text=text)


async def bye_admin(dp):
    text = f'<b>Прощай!</b>'
    await bot.send_message(chat_id=ADMIN_ID, text=text)


@dp.message_handler(commands='start')
async def send_welcome(message: Message):
    """ После получения команды /start, проверяем зарегистрирован ли пользователь в нашей БД.

    Если пользователь найден, продолжаем общаться с ним показывая кнопки.

    В противном случае, начинаем его регистрировать. В этом обработчике для команды
    /start в поле id класса UserInfo записываем id пользователя извлекая его из сообщения."""

    text_for_existing_user = f'Рад тебя видеть снова, {message.chat.first_name}!'
    text_for_new_user = f'Привет {message.chat.first_name}, я твой бот помощник!\n\nДавай определим из какой ты '\
                        f'группы. Пожалуйста, отправь мне название своей группы.\n\n'\
                        f'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'

    if db.search(User.id == message.chat.id):
        await message.answer(text_for_existing_user, reply_markup=main_menu)
    else:
        await UserInfo.group.set()
        await message.answer(text_for_new_user)


@dp.message_handler(lambda message: message.text == 'Отменить', state=UserInfo.group)
async def cancel_process(message: Message, state: FSMContext):
    """current_state = await state.get_state()

    if current_state is None:
        return

    logging.info('Отменение процесса %r', current_state)"""
    await state.finish()

    text = 'Действие отменено.'

    await message.answer(text, reply_markup=settings_menu)


@dp.message_handler(lambda message: not re.fullmatch(r'[а-яА-Я]{3}\d{2}-\d{2}', message.text), state=UserInfo.group)
async def got_error_group_name(message: Message):
    error_text = 'Ты указал название группы неправильно, пожалуйста соблюдай строгий формат.\n\n'\
                 'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'
    return await message.reply(error_text)


@dp.message_handler(lambda message: re.fullmatch(r'[а-яА-Я]{3}\d{2}-\d{2}', message.text), state=UserInfo.group)
async def true_group_name(message: Message, state: FSMContext):
    await state.update_data(group=message.text.upper())

    async with state.proxy() as data:
        if db.search(User.id == message.chat.id):
            db.update({'id': message.chat.id, 'group': data['group']})
        else:
            db.insert({'id': message.chat.id, 'group': data['group']})

    await state.finish()
    await message.answer('Твой помощник всё запомнил человек, спасибо. Пользуйся функционалом на здоровье!',
                         reply_markup=main_menu)


# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')


@dp.message_handler(text='Главное меню')
async def show_main_menu(message: Message):
    text = 'Ты вернулся на главное меню.'
    await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text='О боте')
async def show_statistics(message: Message):
    users = len(db)
    text = f'<b>О боте</b>\n\n' \
           f'Пользователей: {users}\n' \
           f'Версия бота: {BOT_VERSION}\n\n' \
           f'Если тебе не удобно пользоваться ботом, ' \
           f'можешь скачать мобильное приложение для <a href="http://sibsau.ru">Android</a> ' \
           f'или <a href="http://sibsau.ru">iOS</a>.'
    await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text='Настройки')
async def show_settings(message: Message):
    text = 'Выбирай что будешь делать.'
    await message.answer(text, reply_markup=settings_menu)


@dp.message_handler(text='Изменить группу')
async def change_group(message: Message):
    current_user = db.search(User.id == message.chat.id)
    # print(current_user)
    current_group = current_user[0]['group']
    text = f'Твоя текущая группа: <b>{current_group}</b>.\n\n' \
           f'Если хочешь изменить группу, пожалуйста отправь ' \
           f'название новой группы.\n\n' \
           f'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'

    await UserInfo.group.set()
    await message.answer(text, reply_markup=changing_group_menu)

