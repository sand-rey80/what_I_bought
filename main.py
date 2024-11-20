import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = FastAPI()


@app.get("/")
async def getget(req: Request):
    print("run get")
    return {"get":"ok"}


@app.post("/")
async def telega():
    print("run post")
    return {"post":"ok"}


async def startBot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    load_dotenv()
    try:
        asyncio.run(startBot())
    except KeyboardInterrupt:
        pass
#    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
#    BOT_TOKEN = os.getenv('BOT_TOKEN')

