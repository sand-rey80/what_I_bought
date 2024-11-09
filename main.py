from fastapi import FastAPI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = FastAPI()


class Data_qr(BaseModel):
    descr: str

@app.get("/")
async def start():
    return {"data":"ok1"}

if __name__ == '__main__':
    load_dotenv()
#    BOT_TOKEN = os.getenv('BOT_TOKEN')

