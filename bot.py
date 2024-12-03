import os
from dotenv import load_dotenv

import json
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import cv2
from pyzbar.pyzbar import decode

from db import DataBaseSession, session_maker, insert_ticket, Ticket, create_tables, drop_all_tables
#import db

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Пришли фото чека. Я попытаюсь распознать и записать результат распознавания в базу')


@dp.message(F.photo)
async def fotka(message: Message):
    link = message.photo[-1].file_id
    tempfile = await bot.download(link, './temp.png')
    img = cv2.imread('./temp.png')
    qr_values = decode(img)
    answer = 'Не удалось прочитать qr-код'
    for i in qr_values:
        qr_data = i.data.decode("utf-8").split('&')
        summa = qr_data[1]
        answer = 'Сумма: ' + summa
        ticket = Ticket()
        ticket.tg_id = message.from_user.id
        ticket.qr_value = json.dumps(qr_data)
        await insert_ticket(session_maker, ticket)
    await message.answer(answer)


async def bot_start(bot):
    print('start bot')
    await create_tables()


async def bot_stop(bot):
    print('stop bot')
    #await drop_all_tables()


async def main():
    dp.startup.register(bot_start)
    dp.shutdown.register(bot_stop)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await dp.start_polling(bot)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass