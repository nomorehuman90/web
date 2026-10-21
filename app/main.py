import json

from fastapi import FastAPI, Request
from starlette.responses import Response

from app.api.routers import board, course, payment, user
from app.db.database import Base, engine
from app.models.board import Board
from app.models.course import Course
from app.models.user import User
from app.models.payment import Payment
from sqlalchemy import inspect, text

app = FastAPI(title="노트 API", version="0.1.0")
@app.middleware("http")
async def response_envelope(request: Request, call_next):
    response = await call_next(request)
    if "application/json" not in response.headers.get("content-type", ""):
        return response

    body = b"".join([chunk async for chunk in response.body_iterator])
    try:
        result = json.loads(body) if body else None
    except (json.JSONDecodeError, UnicodeDecodeError):
        result = body.decode("utf-8", errors="replace")

    if isinstance(result, dict) and {"code", "message", "result"}.issubset(result):
        envelope = result
    else:
        code = response.status_code
        if code < 400:
            message, data = "success", result
        else:
            message = str(result.get("detail", "request failed")) if isinstance(result, dict) else "request failed"
            data = None
        envelope = {"code": code, "message": message, "result": data}

    headers = dict(response.headers)
    headers.pop("content-length", None)
    return Response(
        content=json.dumps(envelope, ensure_ascii=False),
        status_code=response.status_code,
        headers=headers,
        media_type="application/json",
        background=response.background,
    )


app.include_router(user.router)
app.include_router(board.router)
app.include_router(course.router)
app.include_router(payment.router)
Base.metadata.create_all(engine)
with engine.begin() as connection:
    user_columns = {column["name"] for column in inspect(connection).get_columns("user")}
    if "kakao_id" not in user_columns:
        connection.execute(text("ALTER TABLE user ADD COLUMN kakao_id VARCHAR"))

    email_column = next(
        column for column in inspect(connection).get_columns("user") if column["name"] == "email"
    )
    if not email_column["nullable"]:
        connection.exec_driver_sql(
            """
            CREATE TABLE user_email_nullable_migration (
                idx INTEGER NOT NULL PRIMARY KEY,
                email VARCHAR,
                password VARCHAR NOT NULL,
                name VARCHAR NOT NULL,
                kakao_id VARCHAR
            )
            """
        )
        connection.exec_driver_sql(
            """
            INSERT INTO user_email_nullable_migration (idx, email, password, name, kakao_id)
            SELECT idx, email, password, name, kakao_id FROM user
            """
        )
        connection.exec_driver_sql("DROP TABLE user")
        connection.exec_driver_sql(
            "ALTER TABLE user_email_nullable_migration RENAME TO user"
        )

    connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_user_kakao_id ON user (kakao_id)"))


@app.get("/")
def main():
    return {"message": "노트 API 서버입니다."}
