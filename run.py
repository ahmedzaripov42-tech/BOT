import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN, CHANNELS
from bot.handlers import start, post

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(start.router)
    dp.include_router(post.router)
    
    logger.info("=" * 50)
    logger.info("BOT READY")
    logger.info("=" * 50)

    # verify admin status in each configured channel and log connection
    me = await bot.get_me()
    for idx, ch in enumerate(CHANNELS, start=1):
        cid = ch.get('id')
        name = ch.get('name')
        try:
            member = await bot.get_chat_member(cid, me.id)
            if member.status not in ("administrator", "creator"):
                logger.warning(f"Bot is not an admin in channel {cid} ({name})")
            logger.info(f"CHANNEL CONNECTED: {cid} ({name})")
        except Exception as exc:
            logger.warning(f"Channel check failed ({cid}): {exc}")
            # continue without crashing

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
