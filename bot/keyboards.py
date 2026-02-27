from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_menu():
    """Main admin menu"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 POST YARATISH")]
        ],
        resize_keyboard=True
    )


def get_confirm_keyboard():
    """Confirm/Cancel for preview"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_publish"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_post")
            ]
        ]
    )
