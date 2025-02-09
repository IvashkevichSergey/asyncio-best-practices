DB_USERNAME = "postgres"
DB_PASSWORD = "123"
DB_NAME = "async_db"
DB_HOST = "127.0.0.1"
DB_PORT = 5432

connection_settings = dict(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME
)


# SQL команды для создания и наполнения тестовых таблицу

# CREATE_BRAND_TABLE = \
# """
# CREATE TABLE IF NOT EXISTS brand(
# brand_id SERIAL PRIMARY KEY,
# brand_name TEXT NOT NULL
# );"""
# """
# CREATE TABLE IF NOT EXISTS product(
# product_id SERIAL PRIMARY KEY,
# product_name TEXT NOT NULL,
# brand_id INT NOT NULL,
# FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
# );"""
# """
# CREATE TABLE IF NOT EXISTS product_color(
# product_color_id SERIAL PRIMARY KEY,
# product_color_name TEXT NOT NULL
# );"""
# """
# CREATE TABLE IF NOT EXISTS product_size(
# product_size_id SERIAL PRIMARY KEY,
# product_size_name TEXT NOT NULL
# );"""
# """
# CREATE TABLE IF NOT EXISTS sku(
# sku_id SERIAL PRIMARY KEY,
# product_id INT NOT NULL,
# product_size_id INT NOT NULL,
# product_color_id INT NOT NULL,
# FOREIGN KEY (product_id)
# REFERENCES product(product_id),
# FOREIGN KEY (product_size_id)
# REFERENCES product_size(product_size_id),
# FOREIGN KEY (product_color_id)
# REFERENCES product_color(product_color_id)
# );"""
# COLOR_INSERT = \
# """
# INSERT INTO product_color VALUES(1, 'Blue');
# INSERT INTO product_color VALUES(2, 'Black');
# """
# SIZE_INSERT = \
# """
# INSERT INTO product_size VALUES(1, 'Small');
# INSERT INTO product_size VALUES(2, 'Medium');
# INSERT INTO product_size VALUES(3, 'Large');
# """
