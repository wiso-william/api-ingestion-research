import requests
from dataclasses import astuple, dataclass


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
    dimensions: dict 
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    reviews: list
    returnPolicy: str
    minimumOrderQuantity: int
    meta: dict
    images: list
    thumbnail: str

response = requests.get(url=url_maker(BASE_URL,1,0)).json()

prodotto = Product(**response["products"][0])

print(astuple(prodotto))