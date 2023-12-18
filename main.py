import argparse
from database import DatabaseManager
from scraper import KimonoScraper
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')
URL = "https://roninwear.pt/kimono-jiu-jitsu-gi-c-64_303_239.html?all=1&filter_stock=nostock&sort_price=0&filter_price=0&cPath=64_303_239&filter_id=0&filter_size=9&filter_color=0"

def simulate_creation() -> None:
    scraper = KimonoScraper(URL)
    db_manager = DatabaseManager()
    kimonos = scraper.scrape()

    for kimono_data in kimonos:
        db_manager.simulate_create_kimono(kimono_data)
        print(kimono_data.print_with_color())

def get_all_without_img() -> None:
    db_manager = DatabaseManager()
    kimonos = db_manager.find_kimonos_without_img()
    for kimono in kimonos:
        print(f"Kimono without image: {kimono.name}")


def run_main_process() -> None:
    scraper = KimonoScraper(URL)
    db_manager = DatabaseManager()

    kimonos = scraper.scrape()
    for kimono_data in kimonos:
        db_manager.create_kimono(kimono_data)
        print(kimono_data.print_with_color())

def main():
     # Set up argument parser
    parser = argparse.ArgumentParser(description='Process some kimonos.')
    parser.add_argument('--mode', choices=['main', 'sim', 'noimg'], default='main', help='Mode of operation')

    # Parse arguments
    args = parser.parse_args()

    if args.mode == 'sim':
        simulate_creation()
    elif args.mode == 'noimg':
        get_all_without_img()
    else:
        # Default to main process
        run_main_process()


if __name__ == '__main__':
    main()


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process some kimonos.')
    parser.add_argument('--mode', choices=['main', 'simulate', 'noimg'], default='main',
                        help='Mode of operation (default: main)')

    # Parse arguments
    args = parser.parse_args()
    db_manager = DatabaseManager()

    if args.mode == 'simulate':
        kimonos = KimonoScraper(URL).scrape()
        simulate_creation(kimonos, db_manager)
    elif args.mode == 'noimg':
        get_all_without_img(db_manager)
    else:
        # Default to main process
        run_main_process()