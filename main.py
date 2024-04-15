import telebot
from configuration import API, swear_words, API_weather

bot = telebot.TeleBot(API)


# Ругающийся бот

@bot.message_handler(content_types='text')
def main(message):
    """
    Функция для ответа и подсчета ответов на "да" и "нет"
    """
    if message.text.strip().lower() == 'нет':
        bot.send_message(message.chat.id, f'{message.text} - Пидора ответ')
    elif message.text.strip().lower() == 'да':
        bot.reply_to(message, 'Пизда')
    # elif message.text


#Погода

@bot.message_handler(commands=['Погода'])
def weather(message):
    city = 'Moscow'
    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}'




bot.polling(none_stop=True)
