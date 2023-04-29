from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def about():
    return 'Rest API service for finance app'