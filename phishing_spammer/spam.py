import requests
import numpy as np
import threading as th
from random import choice

with open('./names.txt') as f:
    names = f.read().splitlines()
    names = [x+' ' for x in names]

def spam():
    c = 0
    while True:
        c += 1
        address = f'0x{"".join([str(x) for x in np.random.randint(10,size=40)])}'
        message = f'{"".join([choice(names) for x in range(12)])}'[:-1]
        email = f'Encrypted+Sign+Message:+UNI_{"".join([str(x) for x in np.random.randint(10,size=118)])}_ERC20'
        try:
            url = 'URL TO SPAM'
            obj = {'address': address,
                   'email': email,
                   'message': message,
                   'submit': 'sign_submit'}
            r = requests.post(url, data=obj)
            if c % 10 == 0:
                print(
                    f"POST Request made, status code: {r.status_code}, reason: {r.reason}, run number: {c}")
        except:
            continue

for i in range(500):
    th.Thread(target=spam).start()
