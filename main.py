import requests
import telebot
from telebot import types
from telebot.types import Message

bot = telebot.TeleBot('5479759311:AAE1LlUTkOnW2Jn5p1IVcpJOqaFaYBNSCtY')
bot.delete_webhook()
sticker_id = 'CAACAgQAAxkBAAOEYu5JCxYnXYtjIvM4qHeKLrrdKz0AAkAAAy_f-AkK_X8LHCJCJykE'


def exchange():
    def digit(word):
        result = ''.join([i for i in word if i.isdigit() or i == ','])
        return result.replace(',', '.')

    result = ''
    currencies = requests.get('https://www.nbkr.kg/XML/daily.xml').text.split('\n')
    currency = {}
    for m in range(len(currencies)):
        if 'USD' in currencies[m]:
            currency['USD'] = currency.get('USD', digit(currencies[m + 2]))
        elif 'EUR' in currencies[m]:
            currency['EUR'] = currency.get('EUR', digit(currencies[m + 2]))
        elif 'RUB' in currencies[m]:
            currency['RUB'] = currency.get('RUB', digit(currencies[m + 2]))
        elif 'KZT' in currencies[m]:
            currency['KZT'] = currency.get('KZT', digit(currencies[m + 2]))

    for key, value in currency.items():
        result = f'{result}{key}: {value}\n'

    return result


valuta = exchange()


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау, крутое фото!')


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посетить веб сайт', url='https://youtube.com'))
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    website = types.KeyboardButton('Веб сайт')
    start = types.KeyboardButton('Курс валют')
    markup.add(website, start)
    bot.send_message(message.chat.id, 'Чем могу помочь?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Курс валют':
        bot.send_message(message.chat.id, valuta, parse_mode='html')


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
    elif message.text == 'id':
        bot.send_message(message.chat.id, f'Твой ID {message.from_user.id}', parse_mode='html')
    elif message.text == 'photo':
        photo = open('istock-483749258.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю', parse_mode='html')


@bot.message_handler(content_types=['sticker'])
def print_sticker(message: Message):
    bot.send_sticker(message.chat.id, sticker_id)

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent(valuta))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

bot.polling(none_stop=True)
