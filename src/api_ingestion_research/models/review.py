from dataclasses import dataclass

@dataclass(frozen=True)
class Review:
    product_id: int
    rating: int
    comment: str 
    date: str 
    reviewer_name: str
    reviewer_email: str