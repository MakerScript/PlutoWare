import telebot
# import random
# import sys
# import time
from time import gmtime, strftime
from telebot import types
import requests
# from notifiers import get_notifier
from pyfiglet import Figlet
import data.config


# Открытие файлов и чтение их

# mem = open('data/meme.txt', 'r', encoding='UTF-8')
# memis = mem.read().split('\n')
# mem.close()

bot = telebot.TeleBot(data.config.token) # Токен телеграм бота

shrift = Figlet(font='standard')
print(shrift.renderText('Pluto Ware'))


 # Основа бота для использования
@bot.message_handler(commands=['start'])
def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        knopka1 = types.KeyboardButton("/search_ip")
        knopka2 = types.KeyboardButton("/profile")
        knopka3 = types.KeyboardButton("/help")
        knopka4 = types.KeyboardButton("/mem")
        markup.add(knopka1)
        markup.add(knopka2)
        markup.add(knopka3)
        markup.add(knopka4)
        user_name = m.from_user.first_name
        bot.send_message(m.chat.id, f'Здравствуйте {user_name}! \n{strftime("%a, %d %b %Y %H:%M %p", gmtime())}',  reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, '► /start [Запустить бота, сделать рестарт]\n\n► /profile [Посмотреть свой профиль аккаунта] \n\n► /search_ip [Найти по айпи]\n\n► /help [Выводит этот список]')

@bot.message_handler(commands=['profile'])
def settings(msg):
    usid = msg.from_user.id
    usname = msg.from_user.first_name
    usfullname = msg.from_user.full_name
    bot.send_message(msg.chat.id, f'Профиль\n↓ ↓ ↓\n\n├ Полное имя: {usfullname}\n├ Первое имя: {usname}\n├ Айди: {usid}')

@bot.message_handler(commands=['mem'])
def mem(msg):
    bot.send_photo(msg.chat.id, "https://i.ibb.co/H481Tfq/meme1.jpg")
@bot.message_handler(content_types=['text'])
def ipget(m, adr='30.220.218.148'): # рандом айпи
    try:
        zapros = requests.get(url=f'http://ip-api.com/json/{adr}').json() # получаем с сайта в текстовом виде кастомизируем [в виде json]

        data = { # Список из выше ссылки
            '[Айпи]': zapros.get('query'),
            '[Интернет провайдер]': zapros.get('isp'),
            '[Домен]': zapros.get('org'),
            '[Страна]': zapros.get('country'),
            '[Название региона]': zapros.get('regionName'),
            '[Город]': zapros.get('city'),
            '[Зип-код]': zapros.get('zip'),
            '[Широта]': zapros.get('lat'),
            '[Долгота]': zapros.get('lon'),
        }

        for k, v in data.items():
            bot.send_message(m.chat.id, f'{k} : {v}') # Пишем весь список от начала до конца
    except requests.exceptions.ConnectionError:
        bot.send_message(m.chat.id, 'Проверьте пожалуйста свое интернет соединение!') # Если произойдет ошибка


@bot.message_handler(commands=['search_ip'])
def main(msg):
    target_ip = f'{msg.text.strip()}'
    ipget(adr=target_ip)

    if __name__ == '__main__':
        main()





# @bot.message_handler(content_types=["text"])
# def handle_text(message):

bot.polling(none_stop=True, interval=1) # Интервал ответов на команды