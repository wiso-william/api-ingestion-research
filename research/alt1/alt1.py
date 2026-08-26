"""Come alt0 ma voglio flatten i contenuti all interno dei prodotti"""

import requests
from dataclasses import asdict, astuple, dataclass
from typing import Any


BASE_URL = 'https://dummyjson.com/PRODUCTS'
LIMIT = 10
SKIP_AMOUNT = 10

def url_maker(url: str, limit: int, skip:int) -> str:
    return f"{url}/?limit={limit}&skip={skip}"

# start = 0
# for i in range(1,21):
#     url = url_maker(BASE_URL, limit=LIMIT, skip=start)
#     response = requests.get(url=url).json()
#     print(response)
#     start += SKIP_AMOUNT
#     if not response["products"]:
#         break

@dataclass(frozen=True)
class Product:
    id: int
    title: str
    description: str 
    category: str
    price: float
    discountPercentage: float 
    rating: float
    stock: int
    tags: list[str]
    brand: str
    sku: str
    weight: int
    #dimensions: dict
    product_width: float #flat
    product_height: float #flat
    product_depth: float #flat
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    reviews: list
    returnPolicy: str
    minimumOrderQuantity: int
    meta: dict
    images: list
    thumbnail: str

# tags lo lascio come lista dato che ha senso così
# in alternativa potrei creare una tabella con tutti i tag ma per ora va bene così

"""Ho provato a fare così ma non è molto utile se eve stare nella stessa tabella finale"""
# Creo la dataclass per la dimensione del prodotto
# @dataclass(frozen=True)
# class Dimensions:
#     width: float
#     height: float
#     depth: float


response = requests.get(url=url_maker(BASE_URL,1,0)).json()
# dimensione_prodotto = Dimensions(**response["products"][0]["dimensions"])
# print(asdict(dimensione_prodotto))
#prodotto = Product(**response["products"][0])
#print(astuple(prodotto))

"""Questa soluzione è più sensata e non crea problemi di rinominazione"""
def flatten_product_dimensions(product: dict) -> Product:
    dimensions:dict[str, float] = product.pop("dimensions")
    prodotto = Product(**product,
                       product_width=dimensions["width"],
                       product_height=dimensions["height"],
                       product_depth=dimensions["depth"]
                       )
    return prodotto

product = flatten_product_dimensions(response["products"][0])

"""Come puoi vedere questo introduce un problema se vogliamo farlo più volte, vedi alt2 per la risposta"""
# eseguo lo stesso per i metadati
# def flatten_product_metadata(product: dict) -> Product:
#     metadata: dict[str, Any] = product.pop("meta")
#     prodotto = Product(**product,
#     )



print(product)