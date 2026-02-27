from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_admin_menu
from bot.states import PostCreate

router = Router()


@router.message(F.command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Salom! Xush kelibsiz.", reply_markup=get_admin_menu())


@router.message(F.text.in_(["📚 POST YARATISH", "POST YARATISH"]))
async def cmd_start_post(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(PostCreate.waiting_media)
    await message.answer("Surat yoki videoni yuboring.\n(Video 30 daqiqadan oshmasligi kerak.)")
