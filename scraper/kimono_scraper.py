import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys

class KimonoScraper:
    PARENT_CLASS = "prdct-cntd"
    TITLE_CLASS = "prdct-title"
    PRICE_CLASS = "prco prco-s"
    IMG_CLASS = "img-responsive"
    
    def __init__(self, url):
        logging.info("KimonoScraper initialized with URL: %s", self.url)
        self.url = url
        self.kimonos = []

    class KimonoData:
        def __init__(self, name, price, former_price=-1.0, discount=0.0, img='', url='', timestamp=None):
            self.name = name
            self.price = price
            self.former_price = former_price
            self.discount = discount
            self.img = img
            self.url = url
            self.timestamp = timestamp or datetime.now()

        def __str__(self):
            if self.former_price == -1.0:
                return f"{self.name} : Price = {self.price}€ -> {self.url} | {self.timestamp}"
            else:
                strikeout_price = '\u0336'.join(f"{self.former_price}€") + '\u0336'
                return f"{self.name} : Price = {strikeout_price} {self.price}€ | Discount: {self.discount}% -> {self.url} | {self.timestamp}"

    def scrape(self):
        logging.info("Starting scraping process.")
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self._scrape_kimonos(soup)
        return self.kimonos

    def _scrape_kimonos(self, soup):
        logging.info("Processing HTML for scraping.")
        for parent in filter(self._filter_by_pants, soup.find_all("div", class_=self.PARENT_CLASS)):
            kimono = self._generate_kimono(parent)
            logging.info("Appended kimono: %s", kimono)
            self.kimonos.append(kimono)
            self._update_progress("Creating Kimonos", len(self.kimonos) / len(soup.find_all("div", class_=self.PARENT_CLASS)))

    def _generate_kimono(self, element):
        logging.info("Generating KimonoData object for: %s", name)
        name, url, img = self._get_title_url_and_img(element)
        price, former_price, discount = self._get_price(element)
        return self.KimonoData(name, price, former_price, discount, img, url)

    def _filter_by_pants(self, element):
        logging.info("Filtering element: %s", title)
        title = element.find("h3", class_=self.TITLE_CLASS).find("span").text.strip()
        return "Pants" not in title

    def _get_price(self, element):
        logging.info("Extracting price information for: %s", element)
        prices = element.find("div", class_=self.PRICE_CLASS)
        if len(prices.contents) == 1:
            return float(prices.text.strip()[:-1].replace(',', '.')), -1.0, 0.0
        else:
            price_variables = prices.text.strip().split(" ")
            former_price = price_variables[0][:-1].replace(',', '.')
            price = price_variables[1][:-2].replace(',', '.')
            discount = price_variables[2][:-1].replace(',', '.')
            return float(price), float(former_price), float(discount)

    def _get_title_url_and_img(self, element):
        logging.info("Extracting title, URL, and image for: %s", element)
        titles = element.find("h3", class_=self.TITLE_CLASS)
        title_value = titles.find("span")
        url = titles.find("a", href=True)['href']
        img = element.find("img", class_=self.IMG_CLASS)['src']
        return title_value.text.strip(), url, img

    @staticmethod
    def _update_progress(job_title, progress):
        logging.info("Scraping progress: %s%%", round(progress * 100, 2))
        length = 100
        block = int(round(length * progress))
        msg = f"\r{job_title}: [{'#' * block}{'-' * (length - block)}] {round(progress * 100, 2)}%"
        if progress >= 1: msg += " DONE\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()
