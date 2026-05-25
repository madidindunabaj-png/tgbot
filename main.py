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
import easyocr
from PIL import Image
import io

BOT_TOKEN = os.getenv("8665836002:AAGLQRR43pc0njylwwK6G-JOTY8uAkjyMDU")
TARGET_LANG = "ru"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

print("Загружается модель OCR...")
reader = easyocr.Reader(['ru', 'en'], gpu=False)

def keep_alive():
    while True:
        try:
            requests.get("https://httpbin.org/get", timeout=10)
            print(f"[{time.strftime('%H:%M:%S')}] Keep-alive")
        except:
            pass
        time.sleep(240)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("👋 Привет! Отправь текст или фото — переведу.")

@dp.message(F.text)
async def translate_text(message: Message):
    try:
        translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(message.text)
        await message.reply(f"🔄 Перевод:\n\n{translated}")
    except:
        await message.reply("❌ Ошибка перевода")

@dp.message(F.photo)
async def translate_photo(message: Message):
    await message.answer("🔍 Распознаю текст...")
    try:
        photo = message.photo[-1]
        photo_file = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(photo_file.file_path)
        
        image = Image.open(io.BytesIO(photo_bytes.read()))
        result = reader.readtext(image)
        text = " ".join([t[1] for t in result])
        
        if not text.strip():
            await message.reply("❌ Текст не найден")
            return
            
        await message.reply(f"📝 Распознанный текст:\n\n{text[:700]}")
        translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(text)
        await message.reply(f"🔄 Перевод:\n\n{translated}")
    except Exception as e:
        await message.reply("❌ Ошибка")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Бот запущен на Render!")
    threading.Thread(target=keep_alive, daemon=True).start()
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
