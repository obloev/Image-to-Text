import asyncio
import logging
from io import BytesIO

import pytesseract
from PIL import Image
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, loop=loop)


async def on_startup(dispatcher):
    tg_bot = dispatcher.bot
    await tg_bot.send_message(ADMIN_ID, 'Bot started ...')


async def on_shutdown(dispatcher):
    tg_bot = dispatcher.bot
    await tg_bot.send_message(ADMIN_ID, 'Bot stopped ...')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def ocr(message: types.Message):
    await message.answer(str(message))
    bio = BytesIO()
    await message.photo[-1].download(bio)
    await message.answer(str(bio))
    with Image.open(bio) as image:
        text = await loop.run_in_executor(None, pytesseract.image_to_string, image)
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
