import telebot
import requests
import json
from configuration import API, swear_words, API_weather


bot = telebot.TeleBot(API)


#Погода

@bot.message_handler(commands=['Погода'])
def weather(message):
    city = 'Moscow'
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        bot.reply_to(message, f'Сейчас погода: {temp}\nОщущается как: {feels_like}')
    else:
        bot.reply_to(message, 'Город не найден')

# Ругающийся бот

@bot.message_handler(content_types='text')
def main(message):
    """
    Функция для ответа и подсчета ответов на "да" и "нет"
    """
    if message.text.strip().lower() == 'нет':
        bot.send_message(message.chat.id, 'Пидора ответ')
    elif message.text.strip().lower() == 'да':
        bot.reply_to(message, 'Пизда')
    # elif message.text


bot.polling(none_stop=True)
