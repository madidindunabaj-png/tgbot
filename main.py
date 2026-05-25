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
from PIL import Image
import io

BOT_TOKEN = os.getenv("8665836002:AAGLQRR43pc0njylwwK6G-JOTY8uAkjyMDU")
TARGET_LANG = "ru"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Keep-alive
def keep_alive():
    while True:
        try:
            requests.get("https://httpbin.org/get", timeout=10)
        except:
            pass
        time.sleep(240)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я бот-переводчик.\n\n"
        "Отправь текст или фото с текстом — переведу."
    )

@dp.message(F.text)
async def translate_text(message: Message):
    try:
        translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(message.text)
        await message.reply(f"🔄 Перевод:\n\n{translated}")
    except:
        await message.reply("❌ Ошибка перевода")

@dp.message(F.photo)
async def translate_photo(message: Message):
    await message.answer("🔍 Распознаю текст на фото... (через онлайн OCR)")
    try:
        # Скачиваем фото
        photo = message.photo[-1]
        photo_file = await bot.get_file(photo.file_id)
        photo_bytes = await bot.download_file(photo_file.file_path)
        
        # Отправляем на бесплатный OCR API
        files = {'file': ('image.jpg', photo_bytes.read(), 'image/jpeg')}
        response = requests.post('https://api.ocr.space/parse/image', 
                               files=files,
                               data={'apikey': 'K83114419388957', 'language': 'rus+eng'})
        
        result = response.json()
        if result.get('OCRExitCode') == 1:
            extracted_text = result['ParsedResults'][0]['ParsedText']
        else:
            extracted_text = ""

        if not extracted_text.strip():
            await message.reply("❌ Не удалось распознать текст на фото.")
            return

        await message.reply(f"📝 Распознанный текст:\n\n{extracted_text[:700]}")

        translated = GoogleTranslator(source='auto', target=TARGET_LANG).translate(extracted_text)
        await message.reply(f"🔄 Перевод:\n\n{translated}")
    except Exception as e:
        await message.reply("❌ Ошибка обработки фото.")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("✅ Бот запущен на Render!")
    threading.Thread(target=keep_alive, daemon=True).start()
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
