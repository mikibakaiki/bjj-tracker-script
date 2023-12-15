from bjj_tracker import KimonoScraper
from database_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')

def main():
    scraper = KimonoScraper("https://roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=1&filter_stock=nostock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0")
    db_manager = DatabaseManager()

    kimonos = scraper.scrape()

    for kimono_data in kimonos:
        db_manager.create_kimono(kimono_data)
        print(kimono_data)

if __name__ == '__main__':
    main()
