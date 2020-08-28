import re

from main import bot, dp, db, User
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from config import ADMIN_ID


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
        await message.answer(text_for_existing_user)
    else:
        await UserInfo.group.set()
        await message.answer(text_for_new_user)


@dp.message_handler(lambda message: not re.fullmatch(r'[а-яА-Я]{3}\d{2}-\d{2}', message.text), state=UserInfo.group)
async def got_error_group_name(message: Message):
    error_text = 'Ты указал название своей группы неправильно, пожалуйста соблюдай строгий формат.\n\n'\
                 'Пример: <b>БПИ19-02</b> или <b>бпи19-02</b>'
    return await message.reply(error_text)


@dp.message_handler(lambda message: re.fullmatch(r'[а-яА-Я]{3}\d{2}-\d{2}', message.text), state=UserInfo.group)
async def true_group_name(message: Message, state: FSMContext):
    await state.update_data(group=message.text.upper())

    async with state.proxy() as data:
        db.insert({'id': message.chat.id, 'group': data['group']})

    await state.finish()
    await message.answer('Спасибо тебе человек, я тебя запомнил. Пользуйся функционалом на здоровье!')

