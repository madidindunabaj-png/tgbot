import asyncio
import logging
import os
import threading
import time
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from deep_translator import GoogleTranslator

BOT_TOKEN = os.getenv("8665836002:AAGLQRR43pc0njylwwK6G-JOTY8uAkjyMDU")
TARGET_LANG = "ru"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def keep_alive():
    while True:
        try:
            requests.get("https://httpbin.org/get", timeout=10)
        except:
            pass
        time.sleep(300)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("👋 Привет! Отправь текст — переведу.\nФото пока не поддерживается в этой версии.")

@dp.message(F.text)
async def translate_text(message: Message):
    try:
        translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(message.text)
        await message.reply(f"🔄 Перевод:\n\n{translated}")
    except:
        await message.reply("❌ Ошибка перевода")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Бот запущен!")
    threading.Thread(target=keep_alive, daemon=True).start()
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())

