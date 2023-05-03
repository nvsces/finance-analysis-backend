from fastapi import FastAPI
from gsheet import GSheet

app = FastAPI()

#@app.get("/gSheet")
#async def fetchGSheetData():
#    gSheet = GSheet()
#    data = await gSheet.fetchData()
#    return data


@app.get("/expenses")
async def expensesGSheetdata():
    gSheet = GSheet()
    data = await gSheet.fetchData()
    print(data)
    costs = data['values'][0]
    values = data['values'][1]
    expenses = []
    for index, nm in enumerate(costs):
        expenses.append({"name":nm, "value":values[index]})
    return expenses
