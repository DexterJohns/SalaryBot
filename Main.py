import telebot
import datetime
import requests
import re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/4.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

bot = telebot.TeleBot('5673337125:AAGQPKmpMk_M9kwGuqMVB5BId_87IhW7jWU')
raw_date = datetime.datetime.now()
param_date=raw_date.strftime("%Y-%m-%d")



@bot.message_handler(commands=['start'])
def start(message):
    mess = f'<b>{message.from_user.first_name}, тут доступны команды :Srv и /Rate; \n \nВведи целую часть полученной зарплаты:</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    mess=message.text
    
    if message.text == ":Srv":
        bot.send_message(message.chat.id, message, 'lxml')

    
    elif mess.isdigit():
        #print (param_date)
         base_url = "https://www.cbcg.me/en/core-functions/financial-and-banking-operations/fx-reference-rates?vazi_od=" + param_date
         #base_url = "https://www.cbcg.me/download.php?date=" + param_date
         print (base_url)
         r= requests.get(base_url, verify=False, timeout=5)
         soup = BeautifulSoup(r.content, "html.parser")
         print (soup)
         str1 = "".join(map(str,soup.find(lambda tag: tag.name == 'tr' and 'USD' in tag.text)))
         str2 = "".join(line.strip() for line in str1.splitlines())
         rate = re.search(r"(\d).(\d{5})",str2) 
         bot.send_message(message.chat.id, f"Date:                   {param_date} \nSalary $:              {message.text}  \nRate USD-EUR:  {rate.group(0)}", parse_mode='html')
 #       write_to_file()
 #       print('Записали в файл')

    elif message.text == "/Rate":
        #bot.send_message(message.from_user.id, f"PRVA:   {get_PRVA_rates()} \nLOVC:  {get_LOVCEN_rates()} \nHIPO:   {get_HIPO_rates()} \nERST:   {get_ERSTE_rates()}\nNLB:    {get_NLB_rates()}", parse_mode='html')
        bot.send_message(message.from_user.id, f"For 1$ u'll get: \n\nPRVA:   {get_PRVA_rates()} \u20ac \nLOVC:  {get_LOVCEN_rates()} \u20ac \nHIPO:   {get_HIPO_rates()} \u20ac \nNLB:    {get_NLB_rates()} \u20ac", parse_mode='html')
         
    else:
        mess = f'<b>{message.from_user.first_name}</b>, я понимаю только целые числа и некоторые команды, введи целую часть полученной зарплаты. Также доступны команды :Srv и /Rate"'
        bot.send_message(message.chat.id, mess, parse_mode='html')
        #get_year_list(2024)
        get_PRVA_rates()
        get_LOVCEN_rates()
        get_HIPO_rates()
        #get_ERSTE_rates() NOPE!!!
        get_NLB_rates()
        #get_CKB_rates() NOPE!!!
        get_ZIRAAT_rates()
        

def write_to_file():
    f = open("Salary_log.txt", "a")
    f.write("Now the file has more content! \n")
    f.close()

def get_rate_list(string):
    regex = re.compile(r'<[^>]+>')
    rate_list = regex.sub(' ', string)
    letterless = re.sub(r"[a-zA-Z]+", '' ,rate_list)
    stripped = letterless.strip()
    pre_list = " ".join(stripped.split())
    list = pre_list.split(" ")
    return list

def get_PRVA_rates():
    url = "https://www.prvabankacg.com/index.php"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    str1 = "".join(map(str,soup.find(lambda tag: tag.name == 'tr' and 'USD' in tag.text)))
    str2 = "".join(line.strip() for line in str1.splitlines())
    str3 = get_rate_list(str2)
    rate = str3[0]
    return rate

def get_LOVCEN_rates():
    url = "https://www.lovcenbanka.me/banka/kursna-lista"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    str1 = "".join(map(str,soup.find(lambda tag: tag.name == 'div' and 'USD' in tag.text)))
    str2 = "".join(line.strip() for line in str1.splitlines())
    str3 = get_rate_list(str2)
    rate = str3[16]
    return rate

def get_HIPO_rates():
    url = "https://www.hipotekarnabanka.com/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    str1 = "".join(map(str,soup.find(lambda tag: tag.name == 'tr' and 'USD' in tag.text)))
    str2 = "".join(line.strip() for line in str1.splitlines())
    str3 = get_rate_list(str2)
    rate = str3[2]
    return rate

def get_ERSTE_rates():
    url = "https://local.erstebank.hr/rproxy/webdocapi/ebmn/fx/current"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    str1 = "".join(map(str,soup.find(string=re.compile("USD"))))
    str2 = str1.replace("},{","}\n{")
    str3 = str2.split("\n")
    str4 = str3[3]
    str5 = re.findall(r"\d+\.\d+", str4)
    rate = str5[0]
    return rate

def get_NLB_rates():
    url = "https://api.nlb.me/v1/exchange-rates/latest?extended_fields=currencies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    str1 = "".join(map(str,soup.find(string=re.compile("USD"))))
    str2 = str1.replace("},{","}\n{")
    str3 = str2.split("\n")
    str4 = str3[10]
    str5 = re.findall(r"\d+\.\d+", str4)
    rate = str5[0]
    return rate

def get_ZIRAAT_rates():
    url = "https://www.ziraatbank.me/tr/GetCurrency"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    str1 = "".join(map(str,soup.find(string=re.compile("USD"))))
    str2 = str1.replace("},{","}\n{")
    str3 = str2.split("\n")
    str4 = str3[27]
    str5 = re.findall(r"\d+\.\d+", str4)
    rate = str5[0]
    return rate

def get_CKB_rates():
    url = "https://www.ckb.me/gradjani/gradjani-home"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    txt = soup.find("div", class_="rate")
    print(txt)
    #str1 = "".join(map(str,soup.find(lambda tag: tag.name == 'tr' and 'USD' in tag.text)))
    #str2 = "".join(line.strip() for line in str1.splitlines())
    #str3 = get_rate_list(str2)
    #rate = str3[0]
    #return rate

def get_year_list(year):
    inputFile = "replyes.txt"
    givenString = str(year)
    year_list = ''
    print('The following lines contain the string {', givenString, '}:')
    # Opening the given file in read-only mode
    with open(inputFile, 'r') as filedata:
        # Traverse in each line of the file
        for line in filedata:
        # Checking whether the given string is found in the line data
            if givenString in line:
        # Print the line, if the given string is found in the current line
                year_list=year_list+line.strip()+'\n'
                #print(line.strip())


                print (year_list)
    #return year_list


bot.polling(none_stop=True)