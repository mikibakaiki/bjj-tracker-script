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
    # add a kimono
    result = find_one_kimono(kimono.name)
    if result != None:
        # This name already exists, result is the kimono i want
        if (result.img == ''):
            # if there's no image, add it.
            result.update(img=kimono.img)
            result.reload()
        result.update(push__price=kimono.price, push__former_price=kimono.former_price,
                      push__discount=kimono.discount, push__timestamp=kimono.timestamp)
        result.reload()

        print(f'{kimono.name} | {kimono.price} | {kimono.former_price} | {
              kimono.discount} | {kimono.timestamp}')
    else:
        # this kimono does not exist
        new_kimono = convert_kimono_data_to_kimono(kimono)
        new_kimono.save()
        print(f'{kimono.name} | {kimono.price} | {kimono.former_price} | {
              kimono.discount} | {kimono.timestamp}')


def find_one_kimono(name) -> Kimono:
    for kimono in Kimono.objects:
        if (kimono.name == name):
            return kimono

    return None


def get_scrapped_kimonos_list():
    kimonos = scrap_roninwear()
    print(f'NAME | CURRENT PRICE | OLD PRICE | DISCOUNT | DATE')
    for k in kimonos:
        create_kimono(k)


def convert_kimono_data_to_kimono(kimono: KimonoData):
    return Kimono(name=kimono.name, price=[kimono.price], former_price=[kimono.former_price], discount=[kimono.discount], img=kimono.img, url=kimono.url, timestamp=[kimono.timestamp])


if __name__ == '__main__':
    get_kimonos()
