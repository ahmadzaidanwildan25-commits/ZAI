from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Chat(BaseModel):
    message:str


@app.get("/")
def root():

    return{

        "assistant":"ZAI",

        "status":"ONLINE"

    }


@app.post("/chat")
def chat(data:Chat):

    return{

        "reply":f"Anda berkata : {data.message}"

    }