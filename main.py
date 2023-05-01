from fastapi import FastAPI
import uvicorn


app = FastAPI()

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



@app.get("/expenses")
def get_expenses():
    return expenses
