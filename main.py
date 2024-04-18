import telebot
import requests
import random
import os
import json

from datetime import datetime as dt
from telebot import types
from configuration import API, non_swear_yes, API_weather, yes_word, no_word


bot = telebot.TeleBot(API)

main_path = os.getcwd()
name_DL = ''

#Погода

# TODO: сделать погоду на любой запрос (не только на команду)

# @bot.message_handler(commands=['work'])
# def main(message):
#     """
#     Основная функция рабочего бота
#     """
#     # Создаем кнопки для выбора
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton('Укажите номер договора', callback_data='naming')
#     markup.row(button1)
#     bot.send_message(message.chat.id, reply_markup=markup)


# @bot.callback_query_handler(func=lambda callback:True)
# def callback_message(callback):
#     global name_DL
#     if callback.data == 'naming':
#         name_DL


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

# @bot.message_handler(content_types='text')
# def main(message):
#     """
#     Функция для работы с текстом
#     """
#     global name_DL
#     text_user = message.text.strip().lower()

#     if text_user in no_word:
#         bot.send_message(message.chat.id, 'Программиста ответ')
#     elif text_user in yes_word:
#         bot.reply_to(message, random.choice(non_swear_yes))
    # elif 'дл' in text_user:
    #     name_DL = text_user.replace('дл', '')
    #     name_DL = name_DL.replace(' ', '')
    #     try:
    #         int(name_DL)
    #     except ValueError:
    #         bot.send_message(message.chat.id, 'Вы ввели невалидный номер ДЛ')
        
    #     if name_DL == '':
    #         bot.send_message(message.chat.id, 'Вы не ввели номер ДЛ')
    #     else:
    #         bot.send_message(message.chat.id, f'Номер ДЛ {name_DL} успешно зарегестрирован')
    # elif message.text == 'обратись к чат-гпт':
    #     response = bot.send_message('ChatGPT_ForTelegramBot', message.text)
    #     chat_id = response.chat.id
    #     message_id = response.message_id
    #     answer = bot.get_chat_messages(chat_id, message_id).text

    #     bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda message: 'дл' in message.text.strip().lower())
def handle_message(message):
    """
    Функция для обработки 'дл'
    """
    global name_DL
    # Извлекаем номер ДЛ из сообщения
    name_DL = message.text.strip().lower().replace('дл', '')
    name_DL = name_DL.replace(' ', '')

    # Проверяем, содержит ли номер ДЛ только цифры
    if not name_DL.isdigit():
        bot.send_message(message.chat.id, 'Вы ввели невалидный номер ДЛ')
        return

    # Регистрируем номер ДЛ и отправляем подтверждение
    bot.send_message(message.chat.id, f'Номер ДЛ {name_DL} успешно зарегистрирован')


@bot.message_handler(content_types=['document'])
def handle_document(message):
    """
    Функция для выгрузки файла
    """
    global main_path, name_DL

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
    
    if not os.path.exists(name_DL):
        os.makedirs(name_DL)

    os.chdir(name_DL)

    with open(f'{date_string}-{file_name}', "wb") as f:
        f.write(downloaded_file)

    os.chdir(main_path)

    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, "Файл загружен")



bot.polling(none_stop=True)
