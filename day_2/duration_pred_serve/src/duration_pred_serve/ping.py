import time

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def ping():
    return "PONG"

@app.get("/xyz")
def xyz():
    return f"xyz test call {time.time()}"