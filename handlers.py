import re
import time
import logging

from tinydb.operations import set
from main import bot, dp, db, User
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from config import ADMIN_ID, BOT_VERSION, SUPPORT
from keyboards import main_menu, settings_menu, changing_group_menu
from timetable_controller import does_group_exist, does_timetable_exist, show_timetable_for_today


# state
class UserInfo(StatesGroup):
    group = State()


# post-state
class Post(StatesGroup):
    text = State()
    confirm = State()


async def notify_admin(dp):
    text = f'<b>Бот запущен!</b>'
    try:
        for admin_id in ADMIN_ID:
            await bot.send_message(chat_id=admin_id, text=text, reply_markup=main_menu)
    except:
        logging.info(f'У администратора {admin_id} бот остановлен.')


async def bye_admin(dp):
    text = f'<b>Бот остановлен!</b>'
    try:
        for admin_id in ADMIN_ID:
            await bot.send_message(chat_id=admin_id, text=text, reply_markup=main_menu)
    finally:
        pass


@dp.message_handler(commands='start')
async def send_welcome(message: Message):
    """ После получения команды /start, проверяем зарегистрирован ли пользователь в нашей БД.
    Если пользователь найден, продолжаем общаться с ним показывая кнопки.
    В противном случае, начинаем его регистрировать.
    """
    text_for_existing_user = f'Рад вас видеть снова, {message.chat.first_name}!'
    text_for_new_user = f'Доброго времени суток {message.chat.first_name}, я ваш бот' \
                        f' помощник!\n\nДавайте определим из какой вы ' \
                        f'группы. Пожалуйста, отправьте мне название своей группы.\n\n' \
                        f'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'

    if db.search(User.id == message.chat.id):
        await message.answer(text_for_existing_user, reply_markup=main_menu)
    else:
        await UserInfo.group.set()
        await message.answer(text_for_new_user)


@dp.message_handler(text='/update')
async def update_bot(message: Message):
    update_text = f'Бот обновлён до версии <b>{BOT_VERSION}</b>!'
    await message.answer(update_text, reply_markup=main_menu)


@dp.message_handler(text='/send_post')
async def send_public_post(message: Message):
    text_to_admin = 'Чтобы сделать рассылку, оптравьте текст.'
    not_allowed = 'Вам это делать нельзя! ;)'
    if message.chat.id in ADMIN_ID:
        await Post.text.set()
        await message.answer(text_to_admin, reply_markup=main_menu)
    else:
        await message.answer(not_allowed, reply_markup=main_menu)


@dp.message_handler(state=Post.text)
async def got_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)

    text_before_confirmation = f'Ваш текст получен:\n\n{message.text}\n\n' \
                               f'Если хотите начать рассылку, отправьте ' \
                               f'<b>ДА</b>, для отмены - <b>НЕТ</b>.'
    await Post.confirm.set()
    await message.answer(text_before_confirmation, reply_markup=main_menu)


@dp.message_handler(lambda message: message.text.upper() == 'НЕТ', state=Post.confirm)
async def cancel_publication(message: Message, state: FSMContext):
    await state.finish()
    cancellation_text = 'Действие отменено.'
    await message.answer(cancellation_text, reply_markup=main_menu)


@dp.message_handler(lambda message: message.text.upper() == 'ДА', state=Post.confirm)
async def publish(message: Message, state: FSMContext):
    users = db.all()

    counter = 0
    async with state.proxy() as data:
        for user in users:
            print(user)
            if counter % 10 == 0:
                time.sleep(0.5)
            await bot.send_message(chat_id=user['id'], text=data['text'], reply_markup=main_menu)
            counter += 1

    await state.finish()
    publication_ended_text = f'Рассылка закончена.\n\nВаше сообщение' \
                             f'отправлено <b>{counter}</b> пользователям.'
    await bot.send_message(chat_id=593127562, text=publication_ended_text, reply_markup=main_menu)


@dp.message_handler(lambda message: message.text == 'Отменить', state=UserInfo.group)
async def cancel_process(message: Message, state: FSMContext):
    await state.finish()
    text = 'Действие отменено.'
    await message.answer(text, reply_markup=settings_menu)


@dp.message_handler(lambda message: not re.match(r'[а-яА-Я]{,5}\d{2}-\d{2}', message.text), state=UserInfo.group)
async def got_error_group_name(message: Message):
    error_text = 'Вы указали название группы неправильно, пожалуйста соблюдайте строгий формат.\n\n' \
                 'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'
    return await message.reply(error_text)


@dp.message_handler(lambda message: re.match(r'[а-яА-Я]{,5}\d{2}-\d{2}', message.text), state=UserInfo.group)
async def true_group_name(message: Message, state: FSMContext):
    await state.update_data(group=message.text.upper())
    needed_user = db.search(User.id == message.chat.id)

    async with state.proxy() as data:
        if needed_user:
            db.update(set('group', data['group']), User.id == message.chat.id)
        else:
            db.insert({'id': message.chat.id, 'group': data['group']})

    await state.finish()
    await message.answer('Ваш помощник всё запомнил, спасибо. Пользуйтесь функционалом на здоровье!',
                         reply_markup=main_menu)


@dp.message_handler(text='🏠 Главное меню')
async def show_main_menu(message: Message):
    text = 'Вы вернулись на главное меню.'
    await message.answer(text, reply_markup=main_menu)


@dp.message_handler(text='ℹ️ О боте')
async def show_statistics(message: Message):
    users = len(db)
    text = f'<b>О боте</b>\n\n' \
           f'Пользователей: {users}\n' \
           f'Версия бота: {BOT_VERSION}\n\n' \
           f'Если вам не удобно пользоваться ботом, ' \
           f'можете скачать мобильное приложение для Android ' \
           f'или iOS.'
    await message.answer(text, reply_markup=settings_menu)


@dp.message_handler(text='⚙️ Настройки')
async def show_settings(message: Message):
    text = 'Выбирайте действие.'
    await message.answer(text, reply_markup=settings_menu)


@dp.message_handler(text='👥 Изменить группу')
async def change_group(message: Message):
    current_user = db.search(User.id == message.chat.id)
    current_group = current_user[0]['group']
    text = f'Ваша текущая группа: <b>{current_group}</b>.\n\n' \
           f'Если хотите изменить группу, пожалуйста отправьте ' \
           f'название новой группы.\n\n' \
           f'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'
    await UserInfo.group.set()
    await message.answer(text, reply_markup=changing_group_menu)


@dp.message_handler(text='🚀 Раcписание')
async def show_timetable(message: Message):
    current_user_id = message.chat.id

    # timetable_success_text = 'Попробуйте снова через несколько секунд.'
    timetable_fail_text = f'Раcписание для вашей группы ещё не добавлено.\n\n' \
                          f'Попробуйте через некоторое время или сообщите об ошибке' \
                          f': {SUPPORT}'
    group_not_found_text = 'Кажется ваша группа не существует в нашей базе.\n\n' \
                           'Пожалуйста проверьте её, ' \
                           'изменить группу можно в:\nНастройки -> Изменить'

    if await does_group_exist(current_user_id):
        if await does_timetable_exist(current_user_id):
            current_user = db.search(User.id == message.chat.id)
            current_user_group = current_user[0]['group']
            await show_timetable_for_today(current_user_id, current_user_group)
            # await message.answer(timetable_success_text)
        else:
            await message.answer(timetable_fail_text)
    else:
        await message.answer(group_not_found_text)
