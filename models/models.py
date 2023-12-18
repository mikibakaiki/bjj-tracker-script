from mongoengine import *


class Kimono(Document):
    name = StringField(required=True)
    price = ListField(FloatField(required=True))
    former_price = ListField(FloatField(required=True))
    discount = ListField(FloatField(required=True))
    img = StringField(required=True)
    url = StringField(required=True)
    timestamp = ListField(DateTimeField(required=True))

    def __str__(self) -> str:
        return f"{self.name} | Former Price = {self.former_price} | Price = {self.price} € | Discount: {self.discount}% | {self.img} | {self.url} | Timestamp = {self.timestamp}"


class KimonoDTO:
    # do something here
    name: str
    price: float
    former_price: float
    discount: float
