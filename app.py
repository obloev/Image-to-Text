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


def on_startup():
    bot.send_message(ADMIN_ID, 'Bot started ...')


@dp.message_handler(content_types=[types.ContentTypes.PHOTO])
async def ocr(message: types.Message):
    await message.answer(dumps(message.as_json(), indent=4))
    file = message.photo[-1].download()
    text = image_to_text(file)
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup(), on_shutdown=None)
