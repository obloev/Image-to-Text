import asyncio
import logging
from io import BytesIO

import pytesseract
from PIL import Image
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import API_TOKEN, ADMIN_ID
from database import Database

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, loop=loop)
db = Database()


class Post(StatesGroup):
    post = State()


async def on_startup(dispatcher):
    tg_bot = dispatcher.bot
    await tg_bot.send_message(ADMIN_ID, 'Bot started ...')


async def on_shutdown(dispatcher):
    tg_bot = dispatcher.bot
    await tg_bot.send_message(ADMIN_ID, 'Bot stopped ...')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(content_types=types.ContentType.ANY)
async def add_to_database(message: types.Message):
    user_id = message.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)


@dp.message_handler(commands=['count'])
async def number_of_users(message: types.Message):
    count = await db.total_users_count()
    await message.reply(count)


@dp.message_handler(commands=['post'])
async def number_of_users(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.reply('Send me')
        await Post.post.set()


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Canceled')


@dp.message_handler(state=Post.post)
async def send_post(message: types.Message, state: FSMContext):
    users = await db.get_users()
    sent = 0
    failed = 0
    mes = await message.answer('Sent: {}\nFailed: {}\nTotal: {}'.format(sent, failed, sent + failed))
    async for user in users:
        user_id = user['id']
        try:
            await message.forward(user_id)
            sent += 1
            await mes.edit_text('Sent: {}\nFailed: {}\nTotal: {}'.format(sent, failed, sent + failed))
        except Exception as e:
            print(e)
            failed += 1
            await mes.edit_text('Sent: {}\nFailed: {}\nTotal: {}'.format(sent, failed, sent + failed))
    await mes.edit_text('Complete!\n\nSent: {}\nFailed: {}\nTotal: {}'.format(sent, failed, sent + failed))
    await state.finish()


@dp.message_handler(content_types=types.ContentType.PHOTO)
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def ocr(message: types.Message):
    if message.document:
        if message.document.mime_type.startswith('image'):
            photo = message.document
        else:
            return
    else:
        photo = message.photo[-1]
    bio = BytesIO()
    await photo.download(bio)
    with Image.open(bio) as image:
        text = await loop.run_in_executor(None, pytesseract.image_to_string, image)
    await message.reply(f'{text}\n\n@ImageToTextOKBot')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
