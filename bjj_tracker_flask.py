#!/Users/ctw01992/development/bjj_kimonos_scripts/bin python3

from venv import create
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from datetime import datetime

from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, Session


RONINWEAR = "https://www.roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=1&filter_stock=nostock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0"

# all including without stock
#"https://www.roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=1&filter_stock=stock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0"

# good link
#"https://www.roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=0&filter_stock=stock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0"

# test links
# "https://www.roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=0&filter_stock=stock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=8&filter_color=0"
# https://www.roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?page=2&filter_color=0&filter_size=10&filter_id=0&filter_price=0&sort_price=0&filter_stock=stock&all=0
PRICE_THRESHOLD = 70
KIMONO_SIZE = {'A1': 8, 'A2': 9, 'A3': 10}
parent_class = "prdct-cntd"
title_class = "prdct-title"
price_class = "prco prco-s"

ronin_wear_kimonos = []


class Kimono:
    def __init__(self, name: str, price: float, former_price=0.0, discount=0.0, url='', timestamp = datetime.now()):
        self.name = name
        self.price = price
        self.former_price = former_price
        self.discount = discount
        self.url = url
        self.timestamp = timestamp
    
    def __str__(self) -> str:
        if self.former_price == 0.0:
            return f"{self.name} : Price = {self.price}€ -> {self.url}"
        else :
            strikeout_price = '\u0336'.join(f"{self.former_price}€") + '\u0336'
            return f"{self.name} : Price = {strikeout_price} {self.price}€ | Discount: {self.discount}% -> {self.url}"
    


def kimono_generator(element):
    name, url = get_title_and_url(element)
    price, former_price, discount = get_price(element)

    return Kimono(name, price, former_price, discount, url)


def filter_by_pants(parent_element):
    titles = parent_element.find("h3", class_=title_class)
    title_value = titles.find("span")
    if "Pants" in title_value.text.strip():
        return False
    return True


def get_price(element):
    prices = element.find("div", class_=price_class)

    if len(prices.contents) == 1 :
        return float(prices.text.strip()[:-1].replace(',', '.')),0.0,0.0
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


# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)

#     return conn


# def create_table(conn):
#     query = '''CREATE TABLE IF NOT EXISTS kimonos (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         price REAL NOT NULL,
#         date TEXT NOT NULL,
#         url TEXT NOT NULL
#     )'''
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         print("Table created successfully..")
#         conn.commit()
#     except Error as e:
#         print(e)
    

# def insert_kimono(conn, kimono):
#     query = '''INSERT INTO kimonos (
#             name, price, date, url
#         ) VALUES (
#             ?, ?, ?, ?
#         )'''
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query, (kimono.name, kimono.price, kimono.timestamp, kimono.url))
#         conn.commit()
#         print("Kimono inserted..")
#     except Error as e:
#         print(e)


def scrap(soup):
    
    results = []

    for parent in filter(filter_by_pants, soup.find_all("div", class_=parent_class)):
        results.append(parent)
    
    print("\nKIMONOS\n") 
    print(len(results))

    for res in results:
        ronin_wear_kimonos.append(kimono_generator(res))



Base = declarative_base()

class Kimono(Base):
    __tablename__ = "kimonos"

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    price = Column(Float)
    former_price = Column(Float)
    discount = Column(Float)
    timestamp = Column(Date)
    url = Column(String(2000))

    def __str__(self) -> str:
        if self.former_price == 0.0:
            return f"{self.name} : Price = {self.price}€ -> {self.url}"
        else :
            strikeout_price = '\u0336'.join(f"{self.former_price}€") + '\u0336'
            return f"{self.name} : Price = {strikeout_price} {self.price}€ | Discount: {self.discount}% -> {self.url}"

    def __repr__(self):
        return f"Kimono(id={self.id!r}, name={self.name!r}, price={self.price!r}, former_price={self.former_price!r}, discount={self.discount!r}, date={self.date!r}, url={self.url!r})"


def main():
    
    #page = requests.get(RONINWEAR)

    # parse source
    #soup = BeautifulSoup(page.content, 'html.parser')

    # scrap(soup)    
    
    # conn = create_connection(r'./kimonos_tracker.db')
    # # create tables
    # if conn is not None:
    #     # create projects table
    #     create_table(conn)
    #     for rwk in ronin_wear_kimonos:
    #         print(rwk)

    #         insert_kimono(conn, rwk)
    # else:
    #     print("Error! cannot create the database connection.")

    # conn.close()

    engine = create_engine("sqlite://", echo=True, future=True)

    Base.metadata.create_all(engine)

    with Session(engine) as session:

        spongebob = User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@sqlalchemy.org")],
        )
        sandy = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="sandy@squirrelpower.org"),
            ],
        )
        patrick = User(name="patrick", fullname="Patrick Star")

        session.add_all([spongebob, sandy, patrick])

        session.commit()
    # metadata = db.MetaData()
    # kimonos = db.Table('kimonos', metadata, autoload=True, autoload_with=engine)
    # print(kimonos.columns.keys())
    # print(db.select([kimonos]).where(kimonos.columns.name.like('Tatami')))



if __name__ == '__main__':
    main()