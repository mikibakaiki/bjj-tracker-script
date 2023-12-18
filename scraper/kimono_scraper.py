import logging
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

class KimonoScraper:
    PARENT_CLASS = "prdct-cntd"
    TITLE_CLASS = "prdct-title"
    PRICE_CLASS = "prco prco-s"
    IMG_CLASS = "img-responsive"
    
    def __init__(self, url):
        self.url = url
        self.kimonos = []
        logging.info("KimonoScraper initialized with URL: %s", self.url)

    class KimonoData:
        def __init__(self, name, price, former_price=-1.0, discount=0.0, img='', url='', timestamp=None):
            self.name = name
            self.price = price
            self.former_price = former_price
            self.discount = discount
            self.img = img
            self.url = url
            self.timestamp = timestamp or datetime.now()

        def print_hyperlink(self, url, text) -> str:
            return f'\x1B]8;;{url}\x1B\\{text}\x1B]8;;\x1B\\'
        
        def strike_text(self, text: str) -> str:
            return f'\u001b[9m{text}\u001b[0m'
        
        def print_with_color(self) -> str:
            green, blue, yellow, red, reset = '\033[92m', '\033[94m', '\033[93m', '\033[91m', '\033[0m'
            name_str = f"{green}{self.name}{reset}"
            price_str = f"{self.price}€"
            url_str = f"{blue}{self.url}{reset}" if self.url else "No URL"
            img_str = f"{yellow}{'img ok'}{reset}" if self.img else "No Image"

            if self.former_price != -1.0:
                strikeout_price = f"{self.former_price}€"
                strikeout_price = f"{red}{self.strike_text(strikeout_price)}{reset}"
                discount_str = f" | Discount: {self.discount}%"
                return f"{name_str} : Price = {strikeout_price} {price_str}{discount_str} | {url_str} | {img_str} | {self.timestamp}"
            else:
                return f"{name_str} : Price = {price_str} | {url_str} | {img_str} | {self.timestamp}"

        def __str__(self) -> str:
            name_str = f"{self.name}"
            price_str = f"{self.price}€"
            url_str = f"{self.url}" if self.url else "No URL"
            img_str = f"{self.img}" if self.img else "No Image"

            if self.former_price != -1.0:
                strikeout_price = f"{self.former_price}€"
                strikeout_price = f"{self.strike_text(strikeout_price)}"
                discount_str = f" | Discount: {self.discount}%"
                return f"{name_str} : Price = {strikeout_price} {price_str}{discount_str} | {url_str} | {img_str} | {self.timestamp}"
            else:
                return f"{name_str} : Price = {price_str} | {url_str} | {img_str} | {self.timestamp}"

    def scrape(self)-> List[KimonoData]:
        logging.info("Starting scraping process.")
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self._scrape_kimonos(soup)
        return self.kimonos

    def _scrape_kimonos(self, soup) -> None:
        logging.info("Processing HTML for scraping.")
        for parent in filter(self._filter_by_pants, soup.find_all("div", class_=self.PARENT_CLASS)):
            kimono = self._generate_kimono(parent)
            logging.info("Appended kimono: %s", kimono)
            self.kimonos.append(kimono)
            self._update_progress("Creating Kimonos", len(self.kimonos) / len(soup.find_all("div", class_=self.PARENT_CLASS)))
        self._update_progress("Creating Kimonos", 1)

    def _generate_kimono(self, element) -> KimonoData:
        name, url, img = self._get_title_url_and_img(element)
        img_status = "present" if img else "not present"
        logging.info("Generating KimonoData object for: %s, image is %s", name, img_status)
        price, former_price, discount = self._get_price(element)
        return self.KimonoData(name, price, former_price, discount, img, url)

    def _filter_by_pants(self, element) -> bool:
        title = element.find("h3", class_=self.TITLE_CLASS).find("span").text.strip()
        logging.info("Filtering element: %s", title)
        return "Pants" not in title

    def _get_price(self, element) -> Tuple[float, float, float]:
        logging.info("Extracting price information")
        prices = element.find("div", class_=self.PRICE_CLASS)
        if len(prices.contents) == 1:
            price = float(prices.text.strip()[:-1].replace(',', '.'))
            logging.info("Price: %s | Former Price: %s | Discount: %s", price, -1.0, -1.0)
            return price, -1.0, 0.0
        else:
            price_variables = prices.text.strip().split(" ")
            former_price = float(price_variables[0][:-1].replace(',', '.'))
            price = float(price_variables[1][:-2].replace(',', '.'))
            discount = float(price_variables[2][:-1].replace(',', '.'))
            logging.info("Price: %s | Former Price: %s | Discount: %s", price, former_price, discount)
            return price, former_price, discount

    def _get_title_url_and_img(self, element) -> Tuple[str, str, str]:
        logging.info("Extracting title, URL, and image")
        titles = element.find("h3", class_=self.TITLE_CLASS)
        title_value = titles.find("span").text.strip()
        url = titles.find("a", href=True)['href']
        img = element.find("img", class_=self.IMG_CLASS)['src']
        logging.info("Title: %s | URL: %s | IMG: %s", title_value, url, img)
        return title_value, url, img

    @staticmethod
    def _update_progress(job_title, progress):
        logging.info("Scraping progress: %s%%", round(progress * 100, 2))
        length = 100
        block = int(round(length * progress))
        msg = f"\r{job_title}: [{'#' * block}{'-' * (length - block)}] {round(progress * 100, 2)}%"
        if progress >= 1: msg += " DONE\r\n\n"
        sys.stdout.write(msg)
        sys.stdout.flush()
