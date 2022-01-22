import asyncio
import logging
from json import dumps

from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMIN_ID
from utils import image_to_text

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
    await message.answer(message)
    file = await message.photo[-1].download()
    task = asyncio.create_task(image_to_text(file))
    text = await asyncio.gather(task, return_exceptions=True)
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
