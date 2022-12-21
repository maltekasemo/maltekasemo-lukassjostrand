#Created my_gbg_tramnet.svg with create_network_picture.py in lab2

import requests
import json
from bs4 import BeautifulSoup

html = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'

def create_dict_from_web(html):
    r = requests.get(html)
    soup = BeautifulSoup(r.text, 'lxml')
    tuple = []

    for section in soup.find_all('li', attrs = {'class':'mb-1'}):
        object = section.a.text
        link = section.a['href']
        stop_id = link.split('/')[3]
        stop = object.split('\n')[1].replace(',', '').lstrip()
        stop_link = f'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid={stop_id}'
        tuple.append((stop, stop_link))

    dictionary = dict((stop_name, stop_link) for stop_name, stop_link in tuple)
    return dictionary

def create_json_file(data, filename = "tram-url.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

create_json_file(create_dict_from_web(html))

    






