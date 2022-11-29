from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('mark', 'action', 'post_id')

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать 🔥', callback_data='mark:start:-'),
            InlineKeyboardButton(text='Регистрация 😈', callback_data='mark:reg:-')
        ]
    ]
)

start_keyboard1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать 🔥', callback_data='mark:start:-')
        ]
    ]
)
