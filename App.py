import telebot
from config import keys
from Token import TOKEN
from extensions import ConvercionException, CryptoConverter
import datetime

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать! Я готова помочь Вам конвертировать валюту. \
Чтобы начать работу, введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvercionException('Не верные параметры. Помощь: /help')

        quote, base, amount = values
        total_base = "%.2f" % (float(CryptoConverter.get_price(quote, base, amount)) * float(amount))
    except ConvercionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Конвертирую {quote} в {base}\n{amount} {quote} = {total_base} {base} \nпо курсу \
{CryptoConverter.get_price(quote, base, amount)} \nна дату \
{datetime.datetime.now().strftime("%d-%m-%Y")}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)