#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import re
import datetime as dt
import sqlite3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json

#для парсинга:
def check_connect(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    else:
        print('Страница не найдена')
        
def pull_out_words(spisok, name, s1, s2, k):
    for i in range(len(name)):
        a = re.sub('\n', '', name[i].findAll(s1, s2)[k].text)
        a = re.sub('  ', '', a)
        spisok.append(a)

#для бота
def msg(message):
    vk.method('messages.send', {'user_id': event.user_id, 'message': message, 'random_id': random.randint(0, 2048645)})
    
def get_button(label, color, payload):
    return{"action":{"type": "text", "payload": json.dumps(payload), "label": label}, "color": color}

def make_films_in_form_with_range(filmsss, filmslist):
    co = 0
    string = ''
    for i in filmsss:
        for j in i:
            co +=1
            filmslist.append(j)
            string += str(co) + '. ' + str(j) + "\n"
    return string

def make_string_of_seanses_in_normal_form(seans):
    str1 = ''
    for i in seans:
        for j in i:
            j = j.split(', ')
            print('j=', j)
            for v in j:
                v = v.replace(',', '')
                str1 += v +'\n' 
    return(str1)

def find_object_by_input_number(lst, p):
    for i in lst:
        if int(request)-1 == lst.index(i):
            p = i
    return p

def make_a_list_instead_tuple(tpl, lst):
    lst = []
    for i in tpl:
        for j in i:
            lst.append(j)
    return lst


conn=sqlite3.connect('kinotheatres.db')
cursor=conn.cursor()

def parsing():
    url = 'https://kinoteatr.ru/raspisanie-kinoteatrov/'
    check_connect(url)
    kino = {}
    dictfilms = {}
    address = []
    metro = []
    link = []
    filmsname = []
    janr = []
    dict1 = {}
    time = []
    dates = []
    prices = []
    link1 = []
    theatres = []
    dates11 = []
    metro1 = []

    soup = check_connect(url)
    name = soup.findAll('div', 'cinema_card_wrap_description')
    
    for i in range(len(name)):
        a = re.sub('\n', '', name[i].findAll('h3', 'title movie_card_title')[0].text)
        a = re.sub('  ', '', a)
        theatres.append(a)
        kino[a] = {}

    pull_out_words(address, name, 'span', 'sub_title', 0)
    pull_out_words(metro1, name, 'span', 'sub_title', 1)


    for j in metro1:

        for k in j[1::]:
            if (k.isupper()) and (j[j.find(k)-1] != '-') and(j[j.find(k)-1] != ' '):
                j = j[0:j.find(k)] + ', '+ j[j.find(k)::]
        metro.append(j)

    del metro1

    now = dt.datetime.now()
    for i in range(4):
        next_day = now + dt.timedelta(days = i)
        dates11.append(str(next_day)[:str(next_day).find(' ')])
    for j in dates11:
        j = j.replace('-', '.')[5::] 

        if j[:2:] == '12':
            j = j[3::] + ' '+ 'декабря'
        elif j[:2:] == '01':
            j = j[3::] + ' '+ 'января'
        elif j[:2:] == '02':
            j = j[3::] + ' '+ 'февраля'
        elif j[:2:] == '03':
            j = j[3::] + ' ' + 'марта'
        elif j[:2:] == '04':
            j = j[3::]+ ' ' + 'апреля'
        elif j[:2:] == '05':
            j = j[3::] + ' '+ 'мая'
        elif j[:2:] == '06':
            j = j[3::]+ ' ' + 'июня'
        elif j[:2:] == '07':
            j = j[3::] + ' '+ 'июля'
        elif j[:2:] == '08':
            j = j[3::] + ' '+ 'августа'
        elif j[:2:] == '09':
            j = j[3::]+ ' ' + 'сентября'
        elif j[:2:] == '10':
            j = j[3::] + ' '+ 'октября'
        elif j[:2:] == '11':
            j = j[3::]+ ' ' + 'ноября'
        dates.append(j)

    for i,e in enumerate(kino.keys()):
        kino[e] = {'address': address[i], 'metro': metro[i], 'dates': {k: {} for k in dates}}

    for i, e in enumerate(name):
        a = name[i].select('div.cinema_card_wrap_description a')
        for t in a:
            link.append(t.attrs['href'])

    for h in link:
        h = h+ '?date='
        link1.append(h)
    dates = []

    for d, l in enumerate(link1):
        for c, j in enumerate(dates11):
            q = str(l) +  str(j)
            r = requests.get(q)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
            j = j.replace('-', '.')[5::] 
            if j[:2:] == '12':
                j = j[3::] + ' '+ 'декабря'
            elif j[:2:] == '01':
                j = j[3::] + ' '+ 'января'
            elif j[:2:] == '02':
                j = j[3::] + ' '+ 'февраля'
            elif j[:2:] == '03':
                j = j[3::] + ' ' + 'марта'
            elif j[:2:] == '04':
                j = j[3::]+ ' ' + 'апреля'
            elif j[:2:] == '05':
                j = j[3::] + ' '+ 'мая'
            elif j[:2:] == '06':
                j = j[3::]+ ' ' + 'июня'
            elif j[:2:] == '07':
                j = j[3::] + ' '+ 'июля'
            elif j[:2:] == '08':
                j = j[3::] + ' '+ 'августа'
            elif j[:2:] == '09':
                j = j[3::]+ ' ' + 'сентября'
            elif j[:2:] == '10':
                j = j[3::] + ' '+ 'октября'
            elif j[:2:] == '11':
                j = j[3::]+ ' ' + 'ноября'
            dates.append(j)
            films = soup.findAll('div', class_='shedule_movie bordered gtm_movie')
            for i in range(len(films)):
                a = re.sub('\n', '', films[i].findAll('span', 'movie_card_header title')[0].text)
                a = re.sub('  ', '', a)
                a = re.sub('\'','', a)
                a = re.sub('\"','', a)
                dict1[a] = {}
            for i in range(len(films)):
                a = re.sub('\n', '', films[i].findAll('div', 'shedule_movie_sessions col col-md-8')[0].text)
                a = re.sub('   ', '', a)
                a = re.sub('(Стандарт)|(Премиум)|(IMAX)|(4DX)|(3D 4DX)|(3D IMAX)|(Dolby Atmos)', ',', a)
                time.append(a)
            for i in range(len(films)):
                a = re.sub('\n', '', films[i].findAll('span', 'movie_card_raiting sub_title')[0].text)
                a = re.sub('   ', '', a)
                janr.append(a)
            for i, k in enumerate(dict1.keys()):
                dict1[k] = {'жанр': janr[i],'сеансы': time[i]}
            kino[theatres[d]]['dates'][j]= dict1
    conn=sqlite3.connect('kinotheatres.db')
    cursor=conn.cursor()
    try:
        cursor.execute('create table brand(id_ primary key, name)')
        cursor.execute('insert into brand (id_, name) values (1, "kinoteatr.ru")')
    except:
        pass
    cursor.execute('''CREATE TABLE cinemas(
                        id integer PRIMARY KEY,
                        teathres text,
                        date text,
                        name text,
                        genres text,
                        metro text,
                        address text,
                        session text)''')
    conn.commit()    
    id_ = 1
    metro1 = 'metro'
    address1 = 'address'
    dates1 = 'dates'
    genr = 'жанр'
    seans = 'сеансы'
    for i, e in enumerate(kino):
        for i1, e1 in enumerate(kino[e][dates1]):
            for i2, e2 in enumerate(kino[e][dates1][e1]):
                e2 = e2.replace('\'','')
                e2 = e2.replace('\"', '')
                cursor.execute(f'insert into cinemas (id, teathres, date, genres, metro, address, session, name) values({id_}, "{e}", "{e1}", "{kino[e][dates1][e1][e2][genr]}", "{kino[e][metro1]}", "{kino[e][address1]}", "{kino[e][dates1][e1][e2][seans]}", "{e2}" )')
                id_+=1
    conn.commit()
    
    
try:
    z = cursor.execute('select date from cinemas').fetchall()
except:
    parsing()
    print('я спарсился ыыы')

print(cursor.execute('select date from cinemas').fetchall())
cursor.execute('Select * from cinemas').fetchall
token = "586e1ebfcf53c5d2ca46d72d3c5cb219e87d9c43047f16ebfcba718f77747c1414bcc10f9f79a395ba0f0"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

count = 0
dateslist = []
metrolist = []
metrolist1 = []
filmslist = []
keyboard = {}
d = p = ''

conn=sqlite3.connect('kinotheatres.db')
cursor=conn.cursor()
    
metrooo = set(cursor.execute('select metro from cinemas').fetchall())
datesss = set(list(cursor.execute('select date from cinemas').fetchall()))
dateslist = make_a_list_instead_tuple(datesss, dateslist)
m = make_films_in_form_with_range(metrooo, metrolist)


for event in longpoll.listen():# Основной цикл
    if event.type == VkEventType.MESSAGE_NEW:# Если пришло новое сообщение
        if event.to_me:# Если оно имеет метку для меня( то есть бота)
            request = event.text.lower() # Сообщение от пользователя
        
        
            if (request == "привет") or (count == 0) or (request == "start"):
                сount = 0
                keyboard = {
                    "one_time": True,
                    "buttons": [  [get_button(label = i, color = "primary", payload = "{\"button\": \"1\"}") for i in dateslist]]}
                keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
                keyboard = str(keyboard.decode('utf-8'))
    
                vk.method('messages.send', {'user_id': event.user_id, 'message': 'Привет! Здесь вы можете быстро найти подходящий кинотеатр, выбрать фильм и узнать расписание сеансов.\n Пока я могу добыть информацию не для всех кинотеатров Москвы, но моя база постоянно пополняется&#128522;\n Выберите дату и я смогу помочь вам&#128521;', 'random_id': random.randint(0, 2048645), 'keyboard': keyboard})
                
                count = 1
                
            
            elif count == 1:
                msg('Пожалуйста, введите НОМЕР наиболее подходящего вам района из предложенных ниже&#128521;')
                msg(m)
                
                data = request
                
                count += 1
                
            elif count == 2:
                if ((request.isalpha()) or (int(request)-1 > len(metrolist))) and ((request != 'пока') or (request != 'привет')):
                    msg('Такого номера не существует, попробуйте еще раз&#128521;')
                    count = 2
                    continue
                    
                d = find_object_by_input_number(metrolist, d)

                msg('Кинотетр по выбранному адресу&#128521;:')
                        
                s = set(cursor.execute("select teathres, address from cinemas where metro = (?)", (d,)).fetchall()) 
                msg((str(i) for i in s))
                
                filmsss = set(cursor.execute("select name from cinemas where metro = (?) and date = (?)", (d, data,)).fetchall())
                msg("Вот какие фильмы есть на вашу дату:")
                
                string = make_films_in_form_with_range(filmsss, filmslist)
                
                msg(string)
                msg('Введите номер фильма, который хотите посмотреть, и я выведу вам список сеансов на вашу дату&#128522;')
                count += 1
                
                
            elif  count == 3:
                if ((request.isalpha()) or (int(request)-1 > len(filmslist))) and ((request != 'пока') or (request != 'привет')):
                    msg("К сожалению, такого номера нет в списке, попробуйте еще раз :)")
                    count = 3
                    continue   
                    
                p = find_object_by_input_number(filmslist, p)
                
                seans = cursor.execute("select session from cinemas where metro = (?) and date = (?) and name = (?)", (d, data, p,)).fetchall()
    
                str1 = make_string_of_seanses_in_normal_form(seans)

                msg(str1)
                msg("Если хотите увидеть сеансы другого фильма, введите номер&#128524;")
                
          
            elif request == "привет":
                msg("Приятного просмотра &#128527;")
                count = 0    
                
            elif request == "пока":
                msg("Приятного просмотра &#128527;")
                count = 0

            else:
                msg("Я вас не понимаю пока что, но потом обязательно научусь")
                count = 0


# In[ ]:


cursor.execute('drop table cinemas')

