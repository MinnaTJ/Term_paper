# Data Dictionary
## ecommerce_news_202502.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 1 |  |
| title | object | 1 |  |
| summary | object | 1 |  |
| text | object | 1 |  |
| url | object | 1 |  |
| source | object | 1 |  |
| category | object | 1 |  |
## ecommerce_news_202503.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 1 |  |
| title | object | 1 |  |
| summary | object | 1 |  |
| text | object | 1 |  |
| url | object | 1 |  |
| source | object | 1 |  |
| category | object | 1 |  |
## ecommerce_news_202504.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 4 |  |
| title | object | 4 |  |
| summary | object | 4 |  |
| text | object | 4 |  |
| url | object | 4 |  |
| source | object | 4 |  |
| category | object | 4 |  |
## ecommerce_news_202505.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 3 |  |
| title | object | 3 |  |
| summary | object | 3 |  |
| text | object | 3 |  |
| url | object | 3 |  |
| source | object | 3 |  |
| category | object | 3 |  |
## ecommerce_news_202506.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 2 |  |
| title | object | 2 |  |
| summary | object | 2 |  |
| text | object | 2 |  |
| url | object | 2 |  |
| source | object | 2 |  |
| category | object | 2 |  |
## ecommerce_news_202507.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 2 |  |
| title | object | 2 |  |
| summary | object | 2 |  |
| text | object | 2 |  |
| url | object | 2 |  |
| source | object | 2 |  |
| category | object | 2 |  |
## ecommerce_news_202508.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 4 |  |
| title | object | 4 |  |
| summary | object | 4 |  |
| text | object | 4 |  |
| url | object | 4 |  |
| source | object | 4 |  |
| category | object | 4 |  |
## ecommerce_news_202509.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 7 |  |
| title | object | 7 |  |
| summary | object | 7 |  |
| text | object | 7 |  |
| url | object | 7 |  |
| source | object | 7 |  |
| category | object | 7 |  |
## ecommerce_news_202510.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 6 |  |
| title | object | 6 |  |
| summary | object | 6 |  |
| text | object | 6 |  |
| url | object | 6 |  |
| source | object | 6 |  |
| category | object | 6 |  |
## ecommerce_news_202511.csv
| field | dtype | non_null | description |
|---|---|---|---|
| published_at | object | 52 |  |
| title | object | 52 |  |
| summary | object | 52 |  |
| text | object | 52 |  |
| url | object | 52 |  |
| source | object | 52 |  |
| category | object | 52 |  |
## olist_customers_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| customer_id | object | 1000 |  |
| customer_unique_id | object | 1000 |  |
| customer_zip_code_prefix | int64 | 1000 |  |
| customer_city | object | 1000 |  |
| customer_state | object | 1000 |  |
## olist_geolocation_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| geolocation_zip_code_prefix | int64 | 1000 |  |
| geolocation_lat | float64 | 1000 |  |
| geolocation_lng | float64 | 1000 |  |
| geolocation_city | object | 1000 |  |
| geolocation_state | object | 1000 |  |
## olist_order_items_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| order_id | object | 1000 |  |
| order_item_id | int64 | 1000 |  |
| product_id | object | 1000 |  |
| seller_id | object | 1000 |  |
| shipping_limit_date | object | 1000 |  |
| price | float64 | 1000 |  |
| freight_value | float64 | 1000 |  |
## olist_order_payments_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| order_id | object | 1000 |  |
| payment_sequential | int64 | 1000 |  |
| payment_type | object | 1000 |  |
| payment_installments | int64 | 1000 |  |
| payment_value | float64 | 1000 |  |
## olist_order_reviews_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| review_id | object | 1000 |  |
| order_id | object | 1000 |  |
| review_score | int64 | 1000 |  |
| review_comment_title | object | 115 |  |
| review_comment_message | object | 436 |  |
| review_creation_date | object | 1000 |  |
| review_answer_timestamp | object | 1000 |  |
## olist_orders_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| order_id | object | 1000 |  |
| customer_id | object | 1000 |  |
| order_status | object | 1000 |  |
| order_purchase_timestamp | object | 1000 |  |
| order_approved_at | object | 1000 |  |
| order_delivered_carrier_date | object | 989 |  |
| order_delivered_customer_date | object | 975 |  |
| order_estimated_delivery_date | object | 1000 |  |
## olist_products_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| product_id | object | 1000 |  |
| product_category_name | object | 971 |  |
| product_name_lenght | float64 | 971 |  |
| product_description_lenght | float64 | 971 |  |
| product_photos_qty | float64 | 971 |  |
| product_weight_g | float64 | 1000 |  |
| product_length_cm | float64 | 1000 |  |
| product_height_cm | float64 | 1000 |  |
| product_width_cm | float64 | 1000 |  |
## olist_sellers_dataset.csv
| field | dtype | non_null | description |
|---|---|---|---|
| seller_id | object | 1000 |  |
| seller_zip_code_prefix | int64 | 1000 |  |
| seller_city | object | 1000 |  |
| seller_state | object | 1000 |  |
