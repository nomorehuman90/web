#클라이언트로부터 받는 데이터의 형식 HTTP 요청
#클라이언트에게 전달해줄 데이터의 형식

from pydantic import BaseModel

#sample
#class User(BaseModel):
#    id: str
#    pw: str

#조회용 요청, 번호
#조회용 응답, 번호, 제목 내용
#작성용 요청, 제목, 내용
#작성용 응답, 번호 제목, 내용


class readReq(BaseModel):
    idx: int

class readRes(BaseModel):
    idx: int
    title: str
    contents: str

class registerReq(BaseModel):
    title: str
    contents: str

class registerRes(BaseModel):
    idx: int
    title: str
    contents: str

class delete(BaseModel):
    idx: int

class update(BaseModel):
    idx: int
    title: str
    contents: str



