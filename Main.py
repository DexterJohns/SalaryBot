import telebot
import datetime
import requests
import re
from bs4 import BeautifulSoup


bot = telebot.TeleBot('5673337125:AAGQPKmpMk_M9kwGuqMVB5BId_87IhW7jWU')
raw_date = datetime.datetime.now()
param_date=raw_date.strftime("%Y-%m-%d")


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'<b>{message.from_user.first_name}, введи целую часть полученной зарплаты:</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    mess=message.text
    
    if message.text == "Serv":
        bot.send_message(message.chat.id, message, parse_mode='html')
    
    elif mess.isdigit():
        base_url = "https://www.cbcg.me/en/core-functions/financial-and-banking-operations/fx-reference-rates?vazi_od=" + param_date
        r= requests.get(base_url)
        soup = BeautifulSoup(r.content, "html.parser")
        str1 = "".join(map(str,soup.find(lambda tag: tag.name == 'tr' and 'USD' in tag.text)))
        str2 = "".join(line.strip() for line in str1.splitlines())
        rate = re.search(r"(\d).(\d{5})",str2) 
        bot.send_message(message.chat.id, f"\nDate:                   {param_date} \nSalary $:              {message.text}  \nRate USD-EUR:  {rate.group(0)}", parse_mode='html')

    #elif mess.isdigit():

    elif message.text == "Export":
        bot.send_message(message.chat.id, "Not working yet :()", parse_mode='html')
        
         
    else:
        mess = f'<b>{message.from_user.first_name}</b>, я понимаю только целые числа, введи целую часть полученной зарплаты:'
        bot.send_message(message.chat.id, mess, parse_mode='html')
        
bot.polling(none_stop=True)