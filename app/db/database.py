# ORM : Object Relation Mapping
# 객체 : 현실 세상의 무언가를 컴퓨터 코드로 옮긴 것
# 개체 : 현실 세상의 무언가를 컴퓨터 데이터로 옮긴 것

#DB 서버와 연결 설정하는 파일

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings
#DB 연결을 관리하는 엔진
engine = create_engine(settings.DATABASE_URL, echo=False)
#DB 작업용 세션을 만드는 도구
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        #return 은 값을 반환하고 함수를 종료하지만 yield 반환하고 일시 중지
        yield db
    finally:
        db.close()



#모델들이 디비 연결하는 곳
class Base(DeclarativeBase):
    pass


