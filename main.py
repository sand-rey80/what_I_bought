import os

from dotenv import load_dotenv

import asyncio

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

import db

import datetime
from typing import List

app = FastAPI()

class TicketORM(BaseModel):
    id: int
    create_date: datetime.datetime
    qr_value: str
    tg_id: str

    class Config:
        from_attributes = True


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tickets", response_model=List[TicketORM])
async def get(date_from, date_to):
    date_df = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    date_dt = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    result = await db.get_tickets( date_df, date_dt)
    await asyncio.sleep(2)
    return result


def main():
    print("main()")
#uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
#uvicorn.run("main:app", port=8000, host="0.0.0.0")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


