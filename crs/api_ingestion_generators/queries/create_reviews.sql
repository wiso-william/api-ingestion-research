CREATE TABLE IF NOT EXISTS reviews
(
    product_id UInt32,
    rating UInt8,
    comment Nullable(String),
    date String,
    reviewerName String,
    reviewerEmail Nullable(String)
)
ENGINE = MergeTree
ORDER BY product_id