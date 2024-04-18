import telebot
import requests
import random
import os
import json

from datetime import datetime as dt
from configuration import API, non_swear_yes, API_weather


bot = telebot.TeleBot(API)
main_path = os.getcwd()

#Погода

# TODO: сделать погоду на любой запрос (не только на команду)

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
    if message.text.strip().lower() == 'нет' or 'ytn':
        bot.send_message(message.chat.id, 'Программиста ответ')
    elif message.text.strip().lower() == 'да' or 'lf':
        bot.reply_to(message, random.choice(non_swear_yes))
    # elif message.text == 'обратись к чат-гпт':
    #     response = bot.send_message('ChatGPT_ForTelegramBot', message.text)
    #     chat_id = response.chat.id
    #     message_id = response.message_id
    #     answer = bot.get_chat_messages(chat_id, message_id).text

    #     bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """
    Функция для выгрузки файла
    """
    global main_path

    file_info = bot.get_file(message.document.file_id)
    file_name = message.document.file_name
    downloaded_file = bot.download_file(file_info.file_path)

    ## Сохраняем файл
    now = dt.now()
    date_string = now.strftime("%m%d%y")

    if date_string in os.listdir():
        os.chdir(date_string)
    else:
        os.mkdir(date_string)
        os.chdir(date_string)

    with open(f'{date_string}-{file_name}', "wb") as f:
        f.write(downloaded_file)

    os.chdir(main_path)

    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, "Файл загружен")
        

bot.polling(none_stop=True)
