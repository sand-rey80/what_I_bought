# import os

# from dotenv import load_dotenv

import asyncio

# import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from bot import update_queue

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
    result = await db.get_tickets(date_df, date_dt)
    await asyncio.sleep(2)
    return result


# Вебхук для обработки входящих сообщений
@app.post("/tghook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()  # Получаем JSON-данные от Telegram
        print(f"Получено обновление: {data}")  # Для отладки

        # Помещаем обновление в очередь
        await update_queue.put(data)

        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    print("Start API main()")
# uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
# uvicorn.run("main:app", port=8000, host="0.0.0.0")

# if __name__ == '__main__':
#    try:
#        asyncio.run(main())
#    except KeyboardInterrupt:
#        pass
