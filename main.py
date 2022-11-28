from dotenv import dotenv_values
from mongoengine import *
from models import Kimono
from bjj_tracker import scrap_roninwear, KimonoData


config = dotenv_values(".env")
kimonos = []

connect(host=f'{config["ATLAS_URI"]}')


def get_kimonos():
    get_scrapped_kimonos_list()
    kimonos.clear()


def create_kimono(kimono: KimonoData):
    print(f'creating kimono {kimono}')
    # add a kimono
    result = find_one_kimono(kimono.name)
    print(f'this is the result -> {result}')
    if result != None:
        # This name already exists, result is the kimono i want
        print(f'There was a kimono found with name {kimono.name}')
        result.update(push__price=kimono.price, push__former_price=kimono.former_price, push__discount=kimono.discount, push__timestamp=kimono.timestamp)
        result.reload()
        print(f'just updated the values for kimono -> {result}')

    else: 
        print(f'no kimono found with name {kimono.name}')
        # this kimono does not exist
        new_kimono = convert_kimono_data_to_kimono(kimono)
        new_kimono.save()
        print(f'just saved the new kimono -> {new_kimono}')


def find_one_kimono(name) -> Kimono :
    for kimono in Kimono.objects:
        if (kimono.name == name):
            return kimono
        
    return None


def get_scrapped_kimonos_list():
    kimonos = scrap_roninwear()
    print("KIMONOS LIST SIZE => ", len(kimonos))
    for k in kimonos:
        create_kimono(k)

def convert_kimono_data_to_kimono(kimono: KimonoData):
    return Kimono(name=kimono.name, price=[kimono.price], former_price=[kimono.former_price], discount=[kimono.discount], url=kimono.url, timestamp=[kimono.timestamp])

if __name__ == '__main__':
    get_kimonos()


# schedule.every().day.at("12:00").do(get_kimonos)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
