from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.board import Board
from app.schemas.board import readRes, registerReq

router = APIRouter(prefix="/board", tags=["board"])


@router.get("/list")
def read_list(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Return a page of posts, newest first."""
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="skip must be non-negative and limit must be between 1 and 100")
    boards = db.scalars(
        select(Board).order_by(Board.idx.desc()).offset(skip).limit(limit)
    ).all()
    return [
        {"idx": board.idx, "title": board.title, "contents": board.contents}
        for board in boards
    ]


@router.get("/read", response_model=readRes)
def read(req: str, db: Session = Depends(get_db)):
    try:
        idx = int(req)
    except ValueError:
        raise HTTPException(status_code=422, detail="req must be a note number")
    board = db.get(Board, idx)
    if board is None:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")
    return board


@router.post("/register", response_model=readRes)
def register(req: registerReq, db: Session = Depends(get_db)):
    board = Board(title=req.title, contents=req.contents)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.get("/delete")
def delete(idx: int, db: Session = Depends(get_db)):
    board = db.get(Board, idx)
    if board is None:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")
    db.delete(board)
    db.commit()
    return {"message": "노트를 삭제했습니다."}


@router.get("/update", response_model=readRes)
def update(idx: int, title: str, contents: str, db: Session = Depends(get_db)):
    board = db.get(Board, idx)
    if board is None:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")
    board.title = title
    board.contents = contents
    db.commit()
    db.refresh(board)
    return board
