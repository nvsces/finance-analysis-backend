import jwt
import psycopg2
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from config import DB_NAME, DB_HOST, DB_PORT, DB_PASS, DB_USER
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class InputCode(BaseModel):
    code: str


class NewSub(BaseModel):
    sub_name: str
    sub_price: int
    sub_currency: str
    sub_date: datetime
    sub_period: str
    fk_subs_users: int


app = FastAPI()
security = HTTPBearer()

connection = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT,
)
connection.autocommit = True



@app.on_event("startup")
async def startup_event():
    print("Сервер запущен")


@app.on_event("shutdown")
async def shutdown_event():
    connection.close()
    print("Сервер остановлен")
@app.post("/login")
async def expensesGSheetdata(item: InputCode):

    code = item.code

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users WHERE code = %s;""",
                (code,)
            )
            data = cursor.fetchone()

            if data:
                user_data = data
                payload = {"id": user_data[0], "username": user_data[1], "tg_id": user_data[2]}
                secret_key = "oeurgoiwehrogouiheroiu"
                token = jwt.encode(payload, secret_key, algorithm="HS256")
                return {"token": token}
            else:
                return {"error": "Пользователь не найден"}
    except Exception as ex:
        print("[INFO] Ошибка при работе с PostgreSQL:", ex)

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials  # Получаем токен из заголовка авторизации

        try:
            secret_key = "oeurgoiwehrogouiheroiu"
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = payload.get("id")
            return user_id
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token",
                headers={"WWW-Authenticate": "Bearer"},  )


        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)



@app.post("/subs")
async def add_subscription(sub: NewSub,user_id: int = Depends(get_current_user_id)):

    try:
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user_data = cursor.fetchone()

            if user_data:

                cursor.execute(
                    """
                    INSERT INTO subs (sub_name, sub_price, sub_currency, sub_date, sub_period, fk_subs_users)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (sub.sub_name, sub.sub_price, sub.sub_currency, sub.sub_date, sub.sub_period, user_id),
                )

                return {"message": "Подписка успешно добавлена."}
            else:
                return {"error": "Пользователь не найден."}

    except Exception as ex:
        print("[INFO] Ошибка при работе с PostgreSQL:", ex)


@app.put("/subs/subId")
async def update_sub(sub_id: int, item: NewSub, user_id: int = Depends(get_current_user_id)):

    sub_name = item.sub_name
    sub_price = item.sub_price
    sub_currency = item.sub_currency
    sub_date = item.sub_date
    sub_period = item.sub_period
    fk_subs_users = item.fk_subs_users

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM subs WHERE id = %s AND fk_subs_users = %s;",
                (sub_id, user_id),
            )
            sub_data = cursor.fetchone()

            if sub_data:

                cursor.execute(
                    """UPDATE subs SET sub_name = %s, sub_price = %s, sub_currency = %s, sub_date = %s,
                     sub_period = %s, fk_subs_users = %s WHERE id = %s;""",
                    (sub_name, sub_price, sub_currency, sub_date, sub_period, fk_subs_users, sub_id)
                )
            return {"done": f"Подписка {sub_id} успешно обновлена!"}

    except Exception as ex:
        print("[INFO] Ошибка при работе с PostgreSQL:", ex)


@app.get("/subs")
async def get_user_subs(user_id: int = Depends(get_current_user_id)):

    try:
        with connection.cursor() as cursor:


            cursor.execute(
                """SELECT * FROM subs WHERE fk_subs_users = %s;""",
                (user_id,)
            )

            subs = cursor.fetchall()

            if subs:

                subs_list = []

                for sub in subs:
                    sub_data = {
                        "sub_name": sub[1],
                        "sub_price": sub[2],
                        "sub_currency": sub[3],
                        "sub_date": sub[4],
                        "sub_period": sub[5],
                        # "fk_subs_users": sub[6]
                    }
                    subs_list.append(sub_data)

                return {"subscriptions": subs_list}
            else:
                return {"subscriptions": []}

    except Exception as ex:
        print("[INFO] Ошибка при работе с PostgreSQL:", ex)


@app.delete("/subs")
async def delete_sub(sub_id: int, user_id: int = Depends(get_current_user_id)):

    try:
        with connection.cursor() as cursor:


            cursor.execute(
                "SELECT * FROM subs WHERE id = %s AND fk_subs_users = %s;",
                (sub_id, user_id),
            )
            sub_data = cursor.fetchone()

            if sub_data:
                cursor.execute(
                    "DELETE FROM subs WHERE id = %s;",
                    (sub_id,),
                )

                return {"message": "Подписка успешно удалена."}
            else:
                return {"error": "Подписка не найдена или не принадлежит пользователю."}


    except Exception as ex:
        print("[INFO] Ошибка при работе с PostgreSQL:", ex)