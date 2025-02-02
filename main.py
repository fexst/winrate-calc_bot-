import telebot
from telebot import types

bot = telebot.TeleBot('')


def create_markup():
    """Создает клавиатуру с вариантами выбора"""
    markup = types.InlineKeyboardMarkup()
    buttons = [
        ('База', 'baza'), ('Б+С', 'bc'), ('С+Б', 'cb'), ('ПОК', 'pok'),
        ('Ордерблок', 'orderb'), ('УСТ', 'ust'), ('РУСТ', 'rust'),
        ('Фигуры', 'fig'), ('Ступени', 'stup'), ('Фибо', 'fibo')
    ]

    for text, callback in buttons:
        markup.add(types.InlineKeyboardButton(text, callback_data=callback))

    return markup


@bot.message_handler(commands=['start'])
def setup1(message):
    """Обработчик команды /start"""
    bot.send_message(
        message.chat.id, 'Выберите сетап:', reply_markup=create_markup()
    )


@bot.callback_query_handler(func=lambda call: True)
def check_callback(call):
    """Обработчик нажатий кнопок"""
    chat_id = call.message.chat.id
    mess = bot.send_message(chat_id, 'Введите общее количество сделок:')
    bot.register_next_step_handler(mess, calculate_winrate, call.data)


def calculate_winrate(message, setup_type):
    """Рассчитывает винрейт"""
    try:
        total_trades = int(message.text)
        mess = bot.send_message(
            message.chat.id, 'Введите количество сделок в плюс:'
        )
        bot.register_next_step_handler(mess, calculate_percentage, setup_type, total_trades)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число.')


def calculate_percentage(message, setup_type, total_trades):
    """Подсчитывает процент успешных сделок"""
    try:
        successful_trades = int(message.text)
        winrate = (successful_trades / total_trades) * 100
        bot.send_message(
            message.chat.id, f'Винрейт {setup_type.upper()} = {winrate:.2f}%'
        )
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Введите число.')


bot.polling(non_stop=True)
