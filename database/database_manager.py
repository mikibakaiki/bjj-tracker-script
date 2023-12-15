import logging
from mongoengine import *
from models import Kimono
from dotenv import dotenv_values

class DatabaseManager:
    def __init__(self):
        logging.info("DatabaseManager initialized. Connected to DB.")
        config = dotenv_values(".env")
        connect(host=config["ATLAS_URI"])

    def find_one_kimono(self, name) -> Kimono:
        logging.info("Searching for kimono: %s", name)
        return Kimono.objects(name=name).first()

    def create_kimono(self, kimono_data):
        kimono = self.find_one_kimono(kimono_data.name)
        if kimono:
            # Update existing kimono
            updates = {
                "push__price": kimono_data.price,
                "push__former_price": kimono_data.former_price,
                "push__discount": kimono_data.discount,
                "push__timestamp": kimono_data.timestamp
            }
            if not kimono.img:
                updates["img"] = kimono_data.img
            kimono.update(**updates)
            kimono.reload()
        else:
            # Create new kimono
            new_kimono = Kimono(
                name=kimono_data.name,
                price=[kimono_data.price],
                former_price=[kimono_data.former_price],
                discount=[kimono_data.discount],
                img=kimono_data.img,
                url=kimono_data.url,
                timestamp=[kimono_data.timestamp]
            )
            new_kimono.save()

    def simulate_create_kimono(self, kimono_data):
        kimono = self.find_one_kimono(kimono_data.name)
        if kimono:
            logging.info("Would update kimono: %s", kimono.name)
            # Simulate updates
        else:
            logging.info("Would create new kimono: %s", kimono_data.name)
            # Simulate creation
        logging.info("Kimono : %s", kimono_data)