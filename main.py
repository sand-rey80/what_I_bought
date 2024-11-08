from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = FastAPI()

@app.get("/")
async def start():
    return {"data":"ok"}

if __name__ == '__main__':
    load_dotenv()
#    BOT_TOKEN = os.getenv('BOT_TOKEN')

