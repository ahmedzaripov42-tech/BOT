from aiogram.fsm.state import StatesGroup, State


class PostCreate(StatesGroup):
    waiting_media = State()
    waiting_caption = State()
    waiting_button_text = State()
    waiting_button_link = State()
    waiting_confirm = State()
