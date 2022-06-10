from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    x = {"message": "HELLO WORLD!!! Welcome to fastAPI!!!"}
    return x

@app.get("/waffle")
def welcome():
    x = {"message": "Belgian Waffle with Fresh Strawberry, extra Chocolate Chips and fresh Whipped Cream"}
    return x
