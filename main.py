from fastapi import FastAPI
from gsheet import GSheet
import uvicorn

expenses = [
    {"name": "Продукты", "value": 3673.5},
    {"name": "Транспорт", "value": 2456},
    {"name": "Рестораны", "value": 34568},
    {"name": "Развлечения", "value": 2452},
    {"name": "Медицина", "value": 2346},
    {"name": "Одежда", "value": 26245},
    {"name": "Бытовая химия", "value": 234},
    {"name": "Корм", "value": 635},
]

app = FastAPI()

@app.get("/gSheet")
async def fetchGSheetData():
    gSheet = GSheet()
    data = await gSheet.fetchData()
    return data


@app.get("/expenses")
def get_expenses():
    return expenses
