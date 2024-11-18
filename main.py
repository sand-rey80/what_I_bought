import uvicorn
from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = FastAPI()


@app.get("/")
async def getget(req: Request):
    print("А")
    return {"ok":"o2"}


@app.post("/")
async def telega():
    print("1111111")
    return {"req":"1"}

if __name__ == '__main__':
    load_dotenv()
#    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
#    BOT_TOKEN = os.getenv('BOT_TOKEN')

