from typing import List
from database import DatabaseManager
from scraper import KimonoScraper
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
URL = "https://roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=1&filter_stock=nostock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0"

def simulate_creation(kimonos: List[KimonoScraper.KimonoData], db_manager: DatabaseManager) -> None:
    for kimono_data in kimonos:
        db_manager.simulate_create_kimono(kimono_data)
        print(kimono_data.print_with_color())

def get_all_without_img(db_manager: DatabaseManager):
    kimonos = db_manager.find_kimonos_without_img()
    for kimono in kimonos:
        print(f"Kimono without image: {kimono.name}")

def main():
    scraper = KimonoScraper(URL)
    db_manager = DatabaseManager()

    kimonos = scraper.scrape()
    for kimono_data in kimonos:
        db_manager.create_kimono(kimono_data)
        print(kimono_data.print_with_color())

if __name__ == '__main__':
    main()
