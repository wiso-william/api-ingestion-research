from dataclasses import dataclass

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
    sku: str
    weight: int
    # flat
    product_width: float 
    product_height: float 
    product_depth: float 
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    returnPolicy: str
    minimumOrderQuantity: int
    # meta: dict
    created_at: str
    updated_at: str
    barcode: str
    qr_code: str
    images: list
    thumbnail: str
    # Default
    brand: str | None = None