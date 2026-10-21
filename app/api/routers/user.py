import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request as UrlRequest, urlopen

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import createToken
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import KakaoLoginReq, LoginReq, LoginRes, SignUpReq, SignUpRes

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/login", response_model=LoginRes)
def login(req: LoginReq, res: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == req.email))
    if user is None or user.kakao_id is not None or user.password != req.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호를 확인해 주세요.")

    res.set_cookie(
        "EN_AT",
        createToken(str(user.idx)),
        httponly=True,
        secure=False,
        samesite="lax",
        domain="en-core.kro.kr"
    )
    return {"user_id": user.idx, "email": user.email, "name": user.name}


@router.post("/signup", response_model=SignUpRes)
def signup(req: SignUpReq, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == req.email))
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 가입된 이메일입니다.")

    new_user = User(email=req.email, password=req.password, name=req.name)
    db.add(new_user)
    db.commit()
    return {"email": new_user.email, "name": new_user.name}


def _kakao_post_form(url: str, values: dict[str, str], access_token: str | None = None) -> dict:
    body = urlencode(values).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    request = UrlRequest(url, data=body, headers=headers, method="POST")
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


@router.post("/kakao/login", response_model=LoginRes)
def kakao_login(req: KakaoLoginReq, res: Response, db: Session = Depends(get_db)):
    if not settings.KAKAO_REST_API_KEY:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Kakao login is not configured.")

    token_values = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "code": req.code,
    }
    if settings.KAKAO_CLIENT_SECRET:
        token_values["client_secret"] = settings.KAKAO_CLIENT_SECRET

    try:
        token_data = _kakao_post_form("https://kauth.kakao.com/oauth/token", token_values)
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Kakao authorization failed.")

        user_request = UrlRequest(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
            method="GET",
        )
        with urlopen(user_request, timeout=10) as response:
            kakao_user = json.loads(response.read().decode("utf-8"))
    except HTTPException:
        raise
    except HTTPError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Kakao authorization failed.") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Could not verify the Kakao account.") from exc

    kakao_id = kakao_user.get("id")
    kakao_account = kakao_user.get("kakao_account") or {}
    nickname = (kakao_account.get("profile") or {}).get("nickname")
    if not kakao_id or not nickname:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Kakao account ID or nickname is unavailable.")

    kakao_id = str(kakao_id)
    user = db.scalar(select(User).where(User.kakao_id == kakao_id))
    if user is None:
        user = User(email=None, password="", name=nickname, kakao_id=kakao_id)
        db.add(user)
    else:
        user.name = nickname

    db.commit()
    res.set_cookie(
        "EN_AT",
        createToken(str(user.idx)),
        httponly=True,
        secure=False,
        samesite="lax",
        domain="en-core.kro.kr",
    )
    return {"user_id": user.idx, "email": user.email, "name": user.name}
