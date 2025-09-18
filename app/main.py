
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import settings
from .handlers import routers
from .models import setup_db

logging.basicConfig(level=logging.INFO)

async def main():
    
    setup_db(settings.db_path)

   
    bot = Bot(
        settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN,  # или ParseMode.HTML, если используешь HTML
            # link_preview_is_disabled=True,
            # protect_content=True,
        ),
    )


    dp = Dispatcher()
    for r in routers:
        dp.include_router(r)

 
    await bot.delete_webhook(drop_pending_updates=True)

 
    try:
        await bot.send_message(settings.admin_chat_id, "✅ Бот запущен и слушает обновления.")
    except Exception as e:
        logging.warning(f"Не удалось отправить стартовое сообщение админу: {e}")

 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
