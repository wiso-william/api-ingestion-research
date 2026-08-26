"""Qui voglio flatten anche metadata"""

"""Come alt0 ma voglio flatten i contenuti all interno dei prodotti"""

import requests
from dataclasses import asdict, astuple, dataclass
from typing import Any


BASE_URL = 'https://dummyjson.com/PRODUCTS'
LIMIT = 10
SKIP_AMOUNT = 10

def url_maker(url: str, limit: int, skip:int) -> str:
    return f"{url}/?limit={limit}&skip={skip}"


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
    # meta: dict
    created_at: str
    updated_at: str
    barcode: str
    qr_code: str
    images: list
    thumbnail: str

response = requests.get(url=url_maker(BASE_URL,1,0)).json()

def flatten_product(product: dict) -> Product:
    # Cosa voglio appiattire ?
    dimensions: dict[str, float] = product["dimensions"]
    metadata: dict[str, Any] = product["meta"]

    # dict comprehension
    return Product(
        **{ # Spacchetto il nuovo dict per avere named argument
            k: v # Valori del nuovo dict
            for k,v in product.items() # items crea pair (id, 2) (nome: Mario)
            if k not in {"dimensions", "meta"} # Condizione + set(migliore per membership)
        },
        # Aggiungo le dimensioni che che mancano
        product_width=dimensions["width"],
        product_height=dimensions["height"],
        product_depth=dimensions["depth"],
        # Aggiungo Metadata
        created_at=metadata["createdAt"],
        updated_at=metadata["updatedAt"],
        barcode=metadata["barcode"],
        qr_code=metadata["qrCode"]
    )

print(flatten_product(response["products"][0]))