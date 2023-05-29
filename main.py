import jwt
import psycopg2
from fastapi_users import fastapi_users, FastAPIUsers

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from gsheet import GSheet
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
import secrets

class Input_code(BaseModel):
    code: str


app = FastAPI()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/expenses")
async def expensesGSheetdata(item: Input_code):
    code = item.code

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            host="178.250.157.195",
            user="admin",
            password="root",
            database='postgres',
            port='9999'
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users WHERE code = %s;""",
                (code,)
            )
            data = cursor.fetchall()

            if data:
                user_data = data[0]
                payload = {"id": user_data[0], "username": user_data[1], "tg_id": user_data[2]}
                secret_key = "oeurgoiwehrogouiheroiu"
                token = jwt.encode(payload, secret_key, algorithm="HS256")
                return token
            else:
                return "Пользователь не найден"

    except Exception as ex:
        print("[INFO] Ошибка при работе с PostgreSQL:", ex)


    # gSheet = GSheet()
    # data = await gSheet.fetchData()
    # print(data)
    # costs = data['values'][0]
    # values = data['values'][1]
    # expenses = []
    # for index, nm in enumerate(costs):
    #     expenses.append({"name":nm, "value":values[index]})
    # return expenses


# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )
#
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )
#
#
# current_user = fastapi_users.current_user()
#
# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"