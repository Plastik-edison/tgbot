import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from downloader import downloader

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для скачивания видео из TikTok, Reels и YouTube Shorts.\n"
        "Просто пришли мне ссылку на видео, и я постараюсь его скачать."
    )

@dp.message(F.text.regexp(r'(https?://\S+)'))
async def handle_link(message: types.Message):
    url = message.text
    
    # Send processing message
    status_msg = await message.answer("⏳ Обрабатываю ссылку... Пожалуйста, подождите.")
    
    try:
        # Download video
        video_path = await downloader.download_video(url)
        
        if video_path and os.path.exists(video_path):
            # Send video
            video = FSInputFile(video_path)
            await message.reply_video(video)
            
            # Clean up
            os.remove(video_path)
        else:
            await message.answer("❌ Не удалось скачать видео. Возможно, ссылка не поддерживается или файл слишком большой.")
            
    except Exception as e:
        logging.error(f"Error handling link: {e}")
        await message.answer("❌ Произошла ошибка при обработке видео.")
    
    finally:
        # Delete processing message
        await status_msg.delete()

async def main():
    print("Bot is starting...")
    # Delete webhook to prevent conflicts and drop pending updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
