from fastapi import FastAPI
from gsheet import GSheet

app = FastAPI()

@app.get("/gSheet")
async def fetchGSheetData():
    gSheet = GSheet()
    data = await gSheet.fetchData()
    return data