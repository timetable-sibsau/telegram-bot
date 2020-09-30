from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚀 Раcписание'),
            KeyboardButton(text='⚙️ Настройки'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


old_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Раcписание на сегодня')
        ],
        [
            KeyboardButton(text='Настройки'),
            KeyboardButton(text='О боте')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


settings_menu = ReplyKeyboardMarkup(
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


changing_group_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отменить')
        ]
    ],
    resize_keyboard=True
)
