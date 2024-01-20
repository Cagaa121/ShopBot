import sqlite3 as sql


async def sql_connector():
    con = sql.connect('market.db')
    cur = con.cursor()

    return con, cur


async def create_tables():
    con, cur = await sql_connector()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id BIGINT PRIMARY KEY
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
                title VARCHAR(200),
                size VARCHAR(50),
                color VARCHAR(50),
                price REAL,
                available BOOLEAN,
                category INTEGER,
                img TEXT
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS category(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50)
        )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50),
            link VARCHAR(50),
            channel_id VARCHAR(50)
        )""")


async def get_categories():
    con, cur = await sql_connector()

    data = cur.execute("SELECT * FROM category").fetchall()
    return data


async def get_products(category):
    con, cur = await sql_connector()

    cat = cur.execute("SELECT id FROM category WHERE name = ?", (category,)).fetchone()
    if cat:
        data = cur.execute("SELECT * FROM products WHERE category = ?", (cat[0],)).fetchall()
        return data
    else:
        return False


async def get_products_by_cat_id(cat_id):
    con, cur = await sql_connector()
    data = cur.execute("SELECT * FROM products WHERE category = ?", (cat_id,)).fetchall()
    return data


async def get_product_info(product_id):
    con, cur = await sql_connector()

    product = cur.execute("SELECT * FROM products WHERE title = ?", (product_id,)).fetchone()
    return product


async def get_channels():
    con, cur = await sql_connector()

    channels = cur.execute("SELECT * FROM channels").fetchall()
    return channels


async def create_channel(name, channel_id, link):
    con, cur = await sql_connector()

    cur.execute("INSERT INTO channels (name, channel_id, link) VALUES (?, ?, ?)",
                (name, channel_id, link)
                )
    con.commit()


async def get_channel_info(channel_id):
    con, cur = await sql_connector()

    info = cur.execute("SELECT * FROM channels WHERE channel_id = ?", (channel_id,)).fetchone()
    return info


async def delete_channel_info(channel_id):
    con, cur = await sql_connector()

    cur.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
    con.commit()


async def count_all_users():
    con, cur = await sql_connector()

    users = cur.execute("SELECT COUNT(*) FROM users").fetchone()
    return users[0]


async def get_all_users():
    con, cur = await sql_connector()

    users = cur.execute("SELECT * FROM users").fetchall()
    return users


async def add_user(user_id: int):
    con, cur = await sql_connector()

    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        con.commit()


async def delete_category(cat_id):
    con, cur = await sql_connector()

    cur.execute("DELETE FROM products WHERE category = ?", (cat_id,))
    cur.execute("DELETE FROM category WHERE id = ?", (cat_id,))
    con.commit()


async def create_category(category_name):
    con, cur = await sql_connector()

    cur.execute("INSERT INTO category (name) VALUES (?)", (category_name,))
    con.commit()


async def delete_product_by_id(product_id):
    con, cur = await sql_connector()

    cur.execute("DELETE FROM products WHERE title = ?", (product_id,))
    con.commit()


async def create_product(cat_id, product_img, product_info):
    con, cur = await sql_connector()

    cur.execute(
        "INSERT INTO products (title, size, color, price, category, img) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (product_info[0], product_info[1], product_info[2], product_info[3], cat_id, product_img)
    )
    con.commit()

