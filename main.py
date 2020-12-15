import json
from keyword import iskeyword


class ColorizeMixin:

    repr_color_code = 33

    def __str__(self):
        return f"\033[1;{self.repr_color_code};40m{self.__repr__()}"


class Advert(ColorizeMixin):

    def __init__(self, json_mapping):
        self.__dict__ = JsonTransformer(json_mapping).__dict__
        if not hasattr(self, 'price_'):
            self.price_ = 0
        if self.price_ < 0:
            raise ValueError('price must be >= 0')

    @property
    def price(self):
        return self.price_

    def __repr__(self):
        return f"{self.title} | {self.price} Р"


class JsonTransformer:

    def __init__(self, json_mapping):
        self.json_mapping = json_mapping
        for k, v in json_mapping.items():
            if isinstance(v, dict):
                v = JsonTransformer(v)
            if iskeyword(k) or k == 'price':
                k = k + '_'
            self.__dict__[k] = v

    def __repr__(self):
        return str(self.json_mapping)


if __name__ == '__main__':
    iphone_str = """{ 
        "title": "iPhone X",  
        "price": 100, 
        "location": { 
            "address": "город Самара, улица Мориса Тореза, 50", 
            "metro_stations": ["Спортивная", "Гагаринская"] 
            } 
        } """
    iphone_ad = Advert(json.loads(iphone_str))
    print(iphone_ad.location.address)

    corgi_str = """{ 
        "title": "Вельш-корги", 
        "price": 1000,
        "class": "dogs", 
        "location": { 
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25" 
            } 
        } """
    corgi_ad = Advert(json.loads(corgi_str))
    print(corgi_ad.class_)

    print(corgi_ad)