from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def start_menu_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.row("Kategoriyalar")
    btn.row("Admin bilan aloqa", "Mening malumotlarim")

    return btn


async def category_btn(categories):
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in categories:
        btn.add(
            KeyboardButton(f"{item[1]}")
        )
    btn.add(
        KeyboardButton("Ortga")
    )

    return btn


async def product_btn(total_pages, prev_page, next_page, page, product_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(text=f"⬅️", callback_data=f"prev:{prev_page}"),
        InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data=f"page"),
        InlineKeyboardButton(text=f"➡️", callback_data=f"next:{next_page}"),
        InlineKeyboardButton(text=f"✅ Sotib olish", callback_data=f"buy:{product_id}"),
    )

    return btn


async def product_btn2(total_pages, prev_page, next_page, page, product_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(text=f"⬅️", callback_data=f"prev_2:{prev_page}"),
        InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data=f"page"),
        InlineKeyboardButton(text=f"➡️", callback_data=f"next_2:{next_page}"),
        InlineKeyboardButton(text=f"Ortga", callback_data=f"back_to_product_category"),
        InlineKeyboardButton(text=f"❌", callback_data=f"del_product:{product_id}"),
    )

    return btn


async def client_phone_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(
        KeyboardButton("Telefon raqamingiz", request_contact=True)
    )
    return btn


async def client_geo_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(
        KeyboardButton("Lokatsiya", request_location=True)
    )
    return btn


# admin panel btns
async def admin_panel_btn():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text="Kanal ➕", callback_data="add_channel"),
        InlineKeyboardButton(text="Kategory ➕", callback_data="add_category"),
        InlineKeyboardButton(text="Tovar ➕", callback_data="add_product"),
        InlineKeyboardButton(text="Xabar yo`llash", callback_data="mailing"),
        InlineKeyboardButton(text="Statistika", callback_data="stat"),
    )
    return btn


async def add_channel_btn(channels):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text="➕", callback_data="create_channel"),
        InlineKeyboardButton(text="Ortga", callback_data="back"),
    )

    if channels:
        for item in channels:
            btn.add(
                InlineKeyboardButton(text=f"{item[1]}", callback_data=f"channel:{item[3]}")
            )

    return btn


async def add_category_btn(categories):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text="➕", callback_data="create_category"),
        InlineKeyboardButton(text="Ortga", callback_data="back"),
    )

    if categories:
        for item in categories:
            btn.add(
                InlineKeyboardButton(text=f"{item[1]}", callback_data=f"delete_category:{item[0]}")
            )

    return btn


async def product_category_btn(categories):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text="➕", callback_data="add_product_category"),
        InlineKeyboardButton(text="Ortga", callback_data="back"),
    )

    if categories:
        for item in categories:
            btn.add(
                InlineKeyboardButton(text=f"{item[1]}", callback_data=f"select_category:{item[0]}")
            )

    return btn


async def channel_info_btn(info):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text=f"Ortga", callback_data=f"back"),
        InlineKeyboardButton(text=f"❌", callback_data=f"channel_del:{info[0]}"),
        InlineKeyboardButton(text=f"{info[1]}", url=f"{info[2]}"),
    )
    return btn


async def categories_btn(categories):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text=f"Ortga", callback_data=f"back"),
    )
    if categories:
        for item in categories:
            btn.add(
                InlineKeyboardButton(text=f"{item[1]}", callback_data=f"select_category_add_product:{item[0]}")
            )

    return btn
