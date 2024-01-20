from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyProductState(StatesGroup):
    client_name = State()
    client_phone = State()
    client_geo = State()


class AdminPanelStates(StatesGroup):
    create_channel_state = State()
    mailing = State()
    create_category_state = State()
    product_context = State()
    product_img = State()

