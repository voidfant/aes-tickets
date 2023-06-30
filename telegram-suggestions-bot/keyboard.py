from aiogram.types import ReplyKeyboardMarkup


class StartKeyboard:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Задать вопрос', 'Уведомить', 'Сообщить о проблеме')


class GoBackKeyboard:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Назад')
