#클라이언트로부터 받는 데이터의 형식 HTTP 요청
#클라이언트에게 전달해줄 데이터의 형식

from pydantic import BaseModel

#sample
#class User(BaseModel):
#    id: str
#    pw: str

class SignUpReq(BaseModel):
    email: str
    password: str
    name: str

class SignUpRes(BaseModel):
    email: str
    name: str

class LoginReq(BaseModel):
    email: str
    password: str

class LoginRes(BaseModel):
    user_id: int
    email: str | None = None
    name: str




class KakaoLoginReq(BaseModel):
    code: str
