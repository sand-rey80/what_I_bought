import os

import db
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

import bot

from db import DataBaseSession, session_maker

import datetime
from typing import Dict, List

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = FastAPI()


class TicketORM(BaseModel):
    id: int
    create_date: datetime.datetime
    qr_value: str
    tg_id: str

    class Config:
        from_attributes = True


@app.get("/tickets", response_model=List[TicketORM])
async def get(date_from, date_to):
    date_df = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    date_dt = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    result = await db.get_tickets( date_df, date_dt)
    return  result


@app.post("/")
async def telega():
    print("run post")
    return {"post":"ok"}


async def main():
    await uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
    await bot.main()

if __name__ == '__main__':
    try:
        print('start_app')
        #
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

#    BOT_TOKEN = os.getenv('BOT_TOKEN')

