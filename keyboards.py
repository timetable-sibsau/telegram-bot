from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚀 Раcписание'),
            KeyboardButton(text='⚙️ Настройки'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


SETTINGS_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👥 Изменить группу'),
            KeyboardButton(text='ℹ️ О боте')
        ],
        [
            KeyboardButton(text='🏠 Главное меню')
        ]
    ],
    resize_keyboard=True
)


CHANGING_GROUP_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отменить')
        ]
    ],
    resize_keyboard=True
)
