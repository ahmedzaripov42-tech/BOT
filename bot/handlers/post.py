import logging
from aiogram import Router, F
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.config import CHANNELS
from bot.keyboards import get_admin_menu, get_confirm_keyboard
from bot.states import PostCreate

logger = logging.getLogger(__name__)
router = Router()


def normalize_link(link: str) -> str:
    """Normalize various link formats to full URL"""
    link = link.strip()
    
    if link.startswith('@'):
        username = link[1:]
        return f"https://t.me/{username}"
    elif link.startswith('t.me/'):
        return f"https://{link}"
    elif link.startswith('telegram.me/'):
        return f"https://{link}"
    else:
        return link


def validate_link(link: str) -> bool:
    """Validate that link is in acceptable format"""
    link = link.strip()
    
    if link.startswith('@'):
        return len(link) > 1
    elif link.startswith(('http://', 'https://', 't.me/', 'telegram.me/')):
        return len(link) > 10
    else:
        return False


@router.message(PostCreate.waiting_media, F.photo)
async def handle_photo(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(media_type='photo', file_id=file_id)
    await state.set_state(PostCreate.waiting_caption)
    await message.answer("Caption ni yuboring.")


@router.message(PostCreate.waiting_media, F.video)
async def handle_video(message: Message, state: FSMContext) -> None:
    if message.video and getattr(message.video, 'duration', 0) > 1800:
        return await message.answer("Video 30 daqiqadan oshmasligi kerak.")
    
    file_id = message.video.file_id
    await state.update_data(media_type='video', file_id=file_id)
    await state.set_state(PostCreate.waiting_caption)
    await message.answer("Caption ni yuboring.")


@router.message(PostCreate.waiting_caption, F.text)
async def handle_caption(message: Message, state: FSMContext) -> None:
    caption = message.text or ""
    entities = message.entities or []
    
    await state.update_data(
        caption=caption,
        caption_entities=entities
    )
    await state.set_state(PostCreate.waiting_button_text)
    await message.answer("Tugma nomini yuboring.")


@router.message(PostCreate.waiting_button_text, F.text)
async def handle_button_text(message: Message, state: FSMContext) -> None:
    button_text = (message.text or "").strip()
    
    if not button_text:
        return await message.answer("Tugma nomi bo'sh bo'lishi kerak emas.")
    
    await state.update_data(button_text=button_text)
    await state.set_state(PostCreate.waiting_button_link)
    await message.answer(
        "Tugma havolasini yuboring.\n\n"
        "Qabul qilinadigan formatlar:\n"
        "- https://example.com\n"
        "- http://example.com\n"
        "- t.me/username\n"
        "- @username"
    )


@router.message(PostCreate.waiting_button_link, F.text)
async def handle_button_link(message: Message, state: FSMContext) -> None:
    link = (message.text or "").strip()
    
    if not validate_link(link):
        return await message.answer(
            "Noto'g'ri link. Iltimos, qabul qilinadigan formatda yuboring:\n"
            "- https://example.com\n"
            "- http://example.com\n"
            "- t.me/username\n"
            "- @username"
        )
    
    normalized_link = normalize_link(link)
    await state.update_data(button_link=normalized_link)
    
    data = await state.get_data()
    caption = data.get('caption', 'Post')
    entities = data.get('caption_entities', [])
    button_text = data.get('button_text', 'O\'tish')
    
    try:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text=button_text, url=normalized_link)
            ]]
        )
        
        if data['media_type'] == 'photo':
            preview = await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=data['file_id'],
                caption=caption,
                caption_entities=entities,
                reply_markup=keyboard
            )
        else:
            preview = await message.bot.send_video(
                chat_id=message.chat.id,
                video=data['file_id'],
                caption=caption,
                caption_entities=entities,
                reply_markup=keyboard
            )
        
        await state.update_data(
            preview_message_id=preview.message_id
        )
        
        await state.set_state(PostCreate.waiting_confirm)
        await message.answer("Postni tasdiqlaysizmi?", reply_markup=get_confirm_keyboard())
    except Exception as e:
        logger.error(f"Preview build error: {e}", exc_info=True)
        await message.answer(f"Xatolik: {str(e)}")


@router.callback_query(PostCreate.waiting_confirm, F.data == "confirm_publish")
async def confirm_publish(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    preview_message_id = data.get("preview_message_id")

    if not preview_message_id:
        await callback.message.answer("Xatolik: Preview topilmadi.")
        return

    # Build channel selection keyboard from config.CHANNELS
    buttons = []
    for idx, ch in enumerate(CHANNELS):
        buttons.append([
            InlineKeyboardButton(text=ch.get("name", f"Channel {idx+1}"), callback_data=f"select_channel:{idx}")
        ])
    selection_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.answer("Qaysi kanalga yuborilsin?", reply_markup=selection_kb)


@router.callback_query(PostCreate.waiting_confirm, F.data == "cancel_post")
async def cancel_post(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await callback.message.answer("Post bekor qilindi.", reply_markup=get_admin_menu())


@router.callback_query(PostCreate.waiting_confirm, F.data.startswith("select_channel:"))
async def select_channel(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    preview_message_id = data.get("preview_message_id")
    if not preview_message_id:
        await callback.message.answer("Xatolik: Preview topilmadi.")
        return

    # parse index
    try:
        idx = int(callback.data.split(":", 1)[1])
    except Exception:
        await callback.message.answer("Noto'g'ri kanal tanlandi.")
        return

    if idx < 0 or idx >= len(CHANNELS):
        await callback.message.answer("Noto'g'ri kanal indeksi.")
        return

    target = CHANNELS[idx].get("id")
    button_text = data.get("button_text", "")
    button_link = data.get("button_link", "")
    final_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_link)]])

    try:
        await callback.message.bot.copy_message(
            chat_id=target,
            from_chat_id=callback.message.chat.id,
            message_id=preview_message_id,
            reply_markup=final_button
        )
    except Exception as e:
        logger.error(f"Publish copy error: {e}", exc_info=True)
        await callback.message.answer(f"Joylashtirishda xatolik yuz berdi: {str(e)}")
        return

    await state.clear()
    await callback.message.answer("✅ Post kanalga yuborildi.", reply_markup=get_admin_menu())
