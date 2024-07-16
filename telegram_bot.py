import telebot
import os


from telebot import types
from configuration import API
from datetime import datetime as dt
from excel_data_getter import answer

bot = telebot.TeleBot(API)
main_path = os.getcwd()
name_DL1 = ''
name_DL2 = ''
flag = 1

@bot.message_handler(commands=['start'])
def handle_start(message):

    #Создаем список возможных взаимодействий с ботом
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton('Годовое удорожание')
    button2 = types.KeyboardButton('Разница в ДЛ')
    button3 = types.KeyboardButton('Сумма закрытия')

    keyboard.add(button1, button2, button3)

    # Отправка сообщения с клавиатурой
    bot.reply_to(message, 'Привет! Я бот.', reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global flag

    if message.text == 'Годовое удорожание':
        # Действия при нажатии на кнопку 1
        bot.reply_to(message, 'Ожидается Excel - файл ДЛ. Напишите номер ДЛ, следующим сообщением отправьте Excel - файл.')
        flag = 1

    elif message.text == 'Разница в ДЛ':
        # Действия при нажатии на кнопку 2
        bot.reply_to(message, 'Ожидается 2 Excel - файла ДЛ')
        flag = 2

    elif message.text == 'Сумма закрытия':
        # Действия при нажатии на кнопку 3
        bot.reply_to(message, 'Ожидается Excel - файл ДЛ')
        flag = 3
    
    # TODO: разобраться с флагами
    if flag == 1 or flag == 3:
        bot.register_next_step_handler(message, naming)
    else:
        bot.register_next_step_handler(message, naming)
        


@bot.callback_query_handler(func=lambda message: True)
def naming(message):
    global name_DL1, name_DL2

    # Извлекаем номер ДЛ из сообщения
    name_DL1 = message.text.strip().lower().replace('дл', '').replace(' ', '')

    # Проверяем, содержит ли номер ДЛ только цифры/empty str
    if not name_DL1.isdigit():
        bot.send_message(message.chat.id, message.text)
        return
    bot.register_next_step_handler(message, bot_answer_flag_1)


@bot.callback_query_handler(func=lambda message: True)
def bot_answer_flag_1(message):

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
    
    if not os.path.exists(name_DL1):
        os.makedirs(name_DL1)

    os.chdir(name_DL1)

    with open(f'{date_string}-{file_name}', "wb") as f:
        f.write(downloaded_file)

    answer_bot = answer(os.getcwd() + '\\' + os.listdir()[0], flag=flag)
    os.chdir(main_path)

    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, f"{answer_bot}")

bot.polling()