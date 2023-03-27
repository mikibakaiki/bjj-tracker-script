#!/usr/bin python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time, sys

RONINWEAR = "https://roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=1&filter_stock=nostock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0"


PRICE_THRESHOLD = 70
KIMONO_SIZE = {'A1': 8, 'A2': 9, 'A3': 10}
parent_class = "prdct-cntd"
title_class = "prdct-title"
price_class = "prco prco-s"

ronin_wear_kimonos = []


class KimonoData:
    def __init__(self, name: str, price: float, former_price=-1.0, discount=0.0, url='', timestamp: datetime = None):
        self.name = name
        self.price = price
        self.former_price = former_price
        self.discount = discount
        self.url = url
        self.timestamp = timestamp
    
    def __str__(self) -> str:
        if self.former_price == -1.0:
            return f"{self.name} : Price = {self.price}€ -> {self.url} | {self.timestamp}"
        else :
            strikeout_price = '\u0336'.join(f"{self.former_price}€") + '\u0336'
            return f"{self.name} : Price = {strikeout_price} {self.price}€ | Discount: {self.discount}% -> {self.url} | {self.timestamp}"
    


def update_progress(job_title, progress):
    length = 20 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()

# Test
# for i in range(100):
#     time.sleep(1000)
#     update_progress("Fetching Kimonos...", i/100.0)
# update_progress("Fetching Kimonos...", 1)


def kimono_generator(element):
    name, url = get_title_and_url(element)
    price, former_price, discount = get_price(element)

    return KimonoData(name, price, former_price, discount, url, datetime.now())


def filter_by_pants(parent_element):
    titles = parent_element.find("h3", class_=title_class)
    title_value = titles.find("span")
    if "Pants" in title_value.text.strip():
        return False
    return True


def get_price(element):
    prices = element.find("div", class_=price_class)
    if len(prices.contents) == 1 :
        return float(prices.text.strip()[:-1].replace(',', '.')),-1.0,0.0
    else:
        price_variables = prices.text.strip().split(" ")
        former_price = price_variables[0][:-1].replace(',', '.')
        price = price_variables[1][:-2].replace(',', '.')
        discount = price_variables[2][:-1].replace(',', '.')
        return float(price), float(former_price), float(discount)



def get_title_and_url(element):
    titles = element.find("h3", class_=title_class)
    title_value = titles.find("span")
    url = titles.find("a", href=True)['href']
    return title_value.text.strip(), url


def scrap(soup):
    
    results = []
    # print( len(list(filter(filter_by_pants, soup.find_all("div", class_=parent_class))))
    # for parent, idx in enumerate(list(filter(filter_by_pants, soup.find_all("div", class_=parent_class)))):
    #     print(parent)
    #     results.append(parent)
    for parent in filter(filter_by_pants, soup.find_all("div", class_=parent_class)):
        #print(parent)
        results.append(parent)

    print("\n# OF KIMONOS: ", len(results))

    for idx, res in enumerate(results):
        ronin_wear_kimonos.append(kimono_generator(res))
        time.sleep(0.001)
        update_progress("Creating Kimonos", idx/len(results))
    update_progress("Creating Kimonos", 1)




def scrap_roninwear():
    ronin_wear_kimonos.clear()
    # print(f"@script before running {len(ronin_wear_kimonos)}")
    page = requests.get(RONINWEAR)

    ## parse source
    soup = BeautifulSoup(page.content, 'html.parser')
    scrap(soup)    
    
    # print kimonos
    # for rwk in ronin_wear_kimonos:
    #     print(rwk)

    #print(f"@script after running {len(ronin_wear_kimonos)}")
    return ronin_wear_kimonos



if __name__ == '__main__':
    scrap_roninwear()