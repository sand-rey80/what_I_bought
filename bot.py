import os
from dotenv import load_dotenv

import json
import asyncio
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Update
#from aiogram.utils import exceptions

from pyzbar.pyzbar import decode
from PIL import Image

from db import DataBaseSession, session_maker, insert_ticket, Ticket, create_tables, drop_all_tables


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
update_queue = asyncio.Queue()
semaphore = asyncio.Semaphore(10)

async def external_decode_qr():
    url = 'http://api.qrserver.com/v1/read-qr-code/'
    img = open('./temp.png', 'rb')
    files = {'file': img}
    responce = requests.post(url, data={'MAX_FILE_SIZE': '1048576', }, files = files)
    if responce.status_code == 200:
        result = responce.text
    else:
        result = ''
    return result


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Пришли фото чека. Я попытаюсь распознать и записать результат распознавания в базу')


@dp.message(F.photo)
async def fotka(message: Message):
    link = message.photo[-1].file_id
    tempfile = await bot.download(link, './temp.png')
    img = Image.open('./temp.png')
    #qr_values = await external_decode_qr()
    qr_values = decode(img)
    if type(qr_values) is list:
        for i in qr_values:
            qr_data = i.data.decode("utf-8").split('&')
            summa = qr_data[1]
            answer = 'Сумма: ' + summa
            ticket = Ticket()
            ticket.tg_id = message.from_user.id
            ticket.qr_value = json.dumps(qr_data)
            await insert_ticket(session_maker, ticket)
    else:
        if os.getenv('USE_EXTERNAL_QR_DECODE_SERVICE'):
            qr_values = await external_decode_qr()
        else:
            answer = 'Не удалось прочитать qr-код'
    await message.answer(answer)


async def bot_start(bot):
    print('start bot')
    await create_tables()


async def bot_stop(bot):
    print('stop bot')
    #await drop_all_tables()

async def process_update(update: Update):
    try:
        async with semaphore:  # Ограничиваем количество задач
            await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Ошибка при обработке обновления: {e}")

async def main():
    dp.startup.register(bot_start)
    dp.shutdown.register(bot_stop)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    #await dp.start_polling(bot)
    # Запускаем обработку обновлений из очереди
    try:
        while True:
            update = await update_queue.get()
            await process_update(update)
    except asyncio.CancelledError:
        print("Приложение остановлено")
    except Exception as e:
        print(f"Ошибка в main: {e}")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass