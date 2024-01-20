import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from btn import *
from states import *
from database import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def command_menu(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Ishga tushirish'),
        ]
    )
    await create_tables()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    user_id = message.from_user.id
    await add_user(user_id)
    btn = await start_menu_btn()
    await message.answer("ShopUz Botga xush kelibsiz!", reply_markup=btn)


@dp.message_handler(text="Kategoriyalar")
async def show_category_handler(message: types.Message):
    category = await get_categories()
    btn = await category_btn(category)
    await message.answer("Kategoriyani tanlang:", reply_markup=btn)


@dp.message_handler(text="Ortga")
async def back_handler(message: types.Message):
    await start_bot(message)


@dp.message_handler(text="Admin bilan aloqa")
async def support_handler(message: types.Message):
    await message.answer("Bot admini: @admin")


@dp.callback_query_handler(text_contains="buy")
async def buy_product_callback(call: types.CallbackQuery, state: FSMContext):
    product_id = call.data.split(":")[-1]
    await state.update_data(product_id=product_id)

    await call.message.delete()
    await call.message.answer("Ismingizni kiriting: ")
    await BuyProductState.client_name.set()


@dp.message_handler(content_types=['text'], state=BuyProductState.client_name)
async def get_client_name_state(message: types.Message, state: FSMContext):
    await state.update_data(client_name=message.text)

    btn = await client_phone_btn()
    await message.answer("Telefon raqamingizni kiriting: ", reply_markup=btn)
    await BuyProductState.client_phone.set()


@dp.message_handler(content_types=['contact'], state=BuyProductState.client_phone)
async def get_client_phone_state(message: types.Message, state: FSMContext):
    await state.update_data(client_phone=message.contact.phone_number)

    btn = await client_geo_btn()
    await message.answer("Lokatsiyangizni yuboring: ", reply_markup=btn)
    await BuyProductState.client_geo.set()


@dp.message_handler(content_types=['location'], state=BuyProductState.client_geo)
async def get_client_geo_state(message: types.Message, state: FSMContext):
    geo_link = f"https://www.google.com/maps?q={message.location.latitude},{message.location.longitude}&ll={message.location.latitude},{message.location.longitude}&z=16"

    data = await state.get_data()
    product = await get_product_info(data['product_id'])

    context = f"ID: {message.from_user.id}\nIsm: {data['client_name']}\nTel.Raqam: {data['client_phone']}\n<a href='{geo_link}'>Lokatsiya</a>\n\nTovar nomi: {product[0]}\nRazmer: {product[1]}\nRangi: {product[2]}\nNarxi: {product[3]} so`m"

    await bot.send_message(
        chat_id= -4004163619,
        text=context
    )

    await message.answer("✅ Buyurtmangiz qabul qilindi")
    await start_bot(message)


@dp.callback_query_handler(text_contains='prev_2')
async def prev_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    prev_page = int(call.data.split(":")[-1])

    products = await state.get_data()
    prod = products['products'][prev_page]
    context = f"Nomi: {prod[0]}\nRazmer: {prod[1]}\nRangi: {prod[2]}\nNarxi: {prod[3]}"
    if call.message.caption != context:
        if prev_page > 0:
            btn = await product_btn2(len(products['products']), prev_page - 1, prev_page + 1, prev_page + 1, prod[0])
        else:
            btn = await product_btn2(len(products['products']), prev_page, prev_page + 1, prev_page + 1, prod[0])

        media = types.InputMediaPhoto(media=prod[-1], caption=context)
        await call.message.edit_media(media=media, reply_markup=btn)


@dp.callback_query_handler(text_contains='next_2')
async def next_callback(call: types.CallbackQuery, state: FSMContext):
    next_page = int(call.data.split(":")[-1])
    await call.answer()

    products = await state.get_data()
    if len(products['products']) != next_page:
        prod = products['products'][next_page]
        context = f"Nomi: {prod[0]}\nRazmer: {prod[1]}\nRangi: {prod[2]}\nNarxi: {prod[3]}"
        if call.message.caption != context:
            btn = await product_btn2(len(products['products']), next_page - 1, next_page + 1, next_page + 1, prod[0])

            media = types.InputMediaPhoto(media=prod[-1], caption=context)
            await call.message.edit_media(media=media, reply_markup=btn)


@dp.callback_query_handler(text_contains='prev')
async def prev_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    prev_page = int(call.data.split(":")[-1])

    products = await state.get_data()
    prod = products['products'][prev_page]
    context = f"Nomi: {prod[0]}\nRazmer: {prod[1]}\nRangi: {prod[2]}\nNarxi: {prod[3]}"
    if call.message.caption != context:
        if prev_page > 0:
            btn = await product_btn(len(products['products']), prev_page - 1, prev_page + 1, prev_page + 1, prod[0])
        else:
            btn = await product_btn(len(products['products']), prev_page, prev_page + 1, prev_page + 1, prod[0])

        media = types.InputMediaPhoto(media=prod[-1], caption=context)
        await call.message.edit_media(media=media, reply_markup=btn)


@dp.callback_query_handler(text_contains='next')
async def next_callback(call: types.CallbackQuery, state: FSMContext):
    next_page = int(call.data.split(":")[-1])
    await call.answer()

    products = await state.get_data()
    if len(products['products']) != next_page:
        prod = products['products'][next_page]
        context = f"Nomi: {prod[0]}\nRazmer: {prod[1]}\nRangi: {prod[2]}\nNarxi: {prod[3]}"
        if call.message.caption != context:
            btn = await product_btn(len(products['products']), next_page - 1, next_page + 1, next_page + 1, prod[0])

            media = types.InputMediaPhoto(media=prod[-1], caption=context)
            await call.message.edit_media(media=media, reply_markup=btn)


@dp.message_handler(commands=['admin'])
async def admin_panel_command(message: types.Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        btn = await admin_panel_btn()
        await message.answer("Siz admin paneldasiz:", reply_markup=btn)


@dp.callback_query_handler(text="back")
async def back_to_panel_callback(call: types.CallbackQuery):
    btn = await admin_panel_btn()
    await call.message.edit_text("Siz admin paneldasiz:", reply_markup=btn)


@dp.callback_query_handler(text="add_channel")
async def add_channel_callback(call: types.CallbackQuery):
    channels = await get_channels()
    btn = await add_channel_btn(channels)
    await call.message.edit_text("Kanal qo`shish bo`limi:", reply_markup=btn)


@dp.callback_query_handler(text="add_category")
async def add_category_callback(call: types.CallbackQuery):
    categories = await get_categories()
    btn = await add_category_btn(categories)
    await call.message.edit_text("Category qo`shish bo`limi:", reply_markup=btn)


@dp.callback_query_handler(text_contains='delete_category')
async def delete_category_callback(call: types.CallbackQuery):
    cat_id = call.data.split(":")[-1]
    await delete_category(cat_id)
    await call.answer("✅ Category o`chirildi!", show_alert=True)
    await add_category_callback(call)


@dp.callback_query_handler(text="create_category")
async def create_category_callback(call: types.CallbackQuery):
    await call.message.edit_text("Category nomini kiriting:")
    await AdminPanelStates.create_category_state.set()


@dp.message_handler(content_types=['text'], state=AdminPanelStates.create_category_state)
async def create_category_state(message: types.Message, state: FSMContext):
    category_name = message.text
    await create_category(category_name)
    await message.answer("✅ Category qo`shildi!")
    await state.finish()
    categories = await get_categories()
    btn = await add_category_btn(categories)
    await message.answer("Category qo`shish bo`limi:", reply_markup=btn)


@dp.callback_query_handler(text="create_channel")
async def create_channel_callback(call: types.CallbackQuery):
    await call.message.edit_text(f"Shu formatda kiriting:\n\nKANAL NOMI\nKANAL ID\nKANAL LINK")
    await AdminPanelStates.create_channel_state.set()


@dp.message_handler(content_types=['text'], state=AdminPanelStates.create_channel_state)
async def create_channel_state(message: types.Message, state: FSMContext):
    text = message.text.split("\n")
    if len(text) == 3:
        await create_channel(text[0], text[1], text[2])
        await message.answer("✅ Kanal saqlandi")
        await admin_panel_command(message)
        await state.finish()
    else:
        await message.answer("Siz notug`ri ko`rinishda kiritdingiz! Qaytadan urinib ko`ring")


@dp.callback_query_handler(text_contains="channel_del")
async def delete_channel_callback(call: types.CallbackQuery):
    channel_id = call.data.split(":")[-1]
    await delete_channel_info(channel_id)
    await call.message.edit_text("✅ Kanal o`chirildi")
    btn = await admin_panel_btn()
    await call.message.answer("Siz admin paneldasiz:", reply_markup=btn)


@dp.callback_query_handler(text_contains="channel")
async def channel_info_callback(call: types.CallbackQuery):
    channel_id = call.data.split(":")[-1]
    info = await get_channel_info(channel_id)
    btn = await channel_info_btn(info)
    await call.message.edit_text(f"Kanal: {info[1]}", reply_markup=btn)


@dp.callback_query_handler(text="add_product")
async def add_product_callback(call: types.CallbackQuery):
    categories = await get_categories()
    btn = await product_category_btn(categories)
    await call.message.edit_text(f"Tovarlar kategoriyasi:", reply_markup=btn)


@dp.callback_query_handler(text_contains="del_product")
async def del_product_callback(call: types.CallbackQuery):
    product_id = call.data.split(":")[-1]
    print(product_id)
    await delete_product_by_id(product_id)
    await call.answer("✅ Tovar o`chirildi.", show_alert=True)
    await call.message.delete()

    categories = await get_categories()
    btn = await product_category_btn(categories)
    await call.message.answer(f"Tovarlar kategoriyasi:", reply_markup=btn)


@dp.callback_query_handler(text="add_product_category")
async def add_product_category_callback(call: types.CallbackQuery):
    categories = await get_categories()
    btn = await categories_btn(categories)
    await call.message.edit_text("Kategoriyani tanlang:", reply_markup=btn)


@dp.callback_query_handler(text_contains="select_category_add_product")
async def select_category_add_product_callback(call: types.CallbackQuery, state: FSMContext):
    cat_id = call.data.split(':')[-1]
    await state.update_data(category=cat_id)

    context = ("<em>Namuna:</em>\n\n"
               "Nomi\n"
               "Razmer\n"
               "Rangi\n"
               "Narxi")
    await call.message.edit_text(context)
    await AdminPanelStates.product_context.set()


@dp.message_handler(content_types=['text'], state=AdminPanelStates.product_context)
async def product_context_state(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(product_info=text.split("\n"))

    await message.answer("Tovar rasmini yuborong:")
    await AdminPanelStates.product_img.set()


@dp.message_handler(content_types=['photo'], state=AdminPanelStates.product_img)
async def product_img_state(message: types.Message, state: FSMContext):
    img_id = message.photo[-1].file_id
    data = await state.get_data()
    await create_product(
        cat_id=data['category'],
        product_img=img_id,
        product_info=data['product_info']
    )
    await message.answer("✅ Tovar qo`shildi")
    await state.finish()


@dp.callback_query_handler(text_contains="select_category")
async def select_category_callback(call: types.CallbackQuery, state: FSMContext):
    cat_id = call.data.split(":")[-1]
    products = await get_products_by_cat_id(cat_id)

    if products:
        await state.update_data(products=products)

        context = f"Nomi: {products[0][0]}\nRazmer: {products[0][1]}\nRangi: {products[0][2]}\nNarxi: {products[0][3]}"

        btn = await product_btn2(
            total_pages=len(products),
            prev_page=0,
            next_page=1,
            page=1,
            product_id=products[0][0]
        )
        await call.message.delete()
        await call.message.answer_photo(products[0][-1], caption=context, reply_markup=btn)
    else:
        await call.answer("Bu kategoriyada tovarlar yoq!", show_alert=True)


@dp.callback_query_handler(text="stat")
async def show_bot_statistics_callback(call: types.CallbackQuery):
    users = await count_all_users()
    await call.answer(f"Bot azolari soni: {users}", show_alert=True)


@dp.callback_query_handler(text='mailing')
async def mailing_callback(call: types.CallbackQuery):
    await call.message.edit_text("Xabaringizni yuboring:")
    await AdminPanelStates.mailing.set()


@dp.message_handler(content_types=['text', 'photo', 'video', 'animation', 'document'], state=AdminPanelStates.mailing)
async def mailing_state(message: types.Message, state: FSMContext):
    text = message.html_text
    caption = message.html_text
    btn = message.reply_markup
    content = message.content_type
    users = await get_all_users()

    await state.finish()

    for user in users:

        if content == 'text':
            await bot.send_message(chat_id=user[0], text=text, reply_markup=btn)

        elif content == 'photo':
            await bot.send_photo(chat_id=user[0], photo=message.photo[-1].file_id, caption=caption, reply_markup=btn)

        elif content == 'video':
            await bot.send_video(chat_id=user[0], video=message.video.file_id, caption=caption, reply_markup=btn)

        elif content == 'animation':
            await bot.send_animation(chat_id=user[0], animation=message.animation.file_id, caption=caption,
                                     reply_markup=btn)

        elif content == 'document':
            await bot.send_document(chat_id=user[0], document=message.document.file_id, caption=caption,
                                    reply_markup=btn)

    await message.reply("✅ Xabar barchaga yo`llandi")
    await admin_panel_command(message)


@dp.message_handler(content_types=['text'])
async def get_cat_btn_handler(message: types.Message, state: FSMContext):
    products = await get_products(message.text)

    if products:
        await state.update_data(products=products)

        context = f"Nomi: {products[0][0]}\nRazmer: {products[0][1]}\nRangi: {products[0][2]}\nNarxi: {products[0][3]}"

        btn = await product_btn(
            total_pages=len(products),
            prev_page=0,
            next_page=1,
            page=1,
            product_id=products[0][0]
        )
        await message.answer_photo(products[0][-1], caption=context, reply_markup=btn)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=command_menu)
