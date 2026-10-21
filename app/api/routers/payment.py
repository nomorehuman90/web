import json
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request as UrlRequest, urlopen
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.course import Course
from app.models.payment import Payment
from app.schemas.payment import (
    PaymentCompleteReq,
    PaymentCompleteRes,
    PaymentPrepareReq,
    PaymentPrepareRes,
)

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/prepare", response_model=PaymentPrepareRes)
def prepare_payment(req: PaymentPrepareReq, db: Session = Depends(get_db)):
    course = db.get(Course, req.course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if course.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This course does not require payment")

    payment_id = f"course-{course.id}-{uuid4().hex}"
    payment = Payment(
        payment_id=payment_id,
        course_id=course.id,
        order_name=course.title,
        amount=course.price,
        status="READY",
    )
    db.add(payment)
    db.commit()
    return PaymentPrepareRes(
        payment_id=payment_id,
        order_name=course.title,
        total_amount=course.price,
    )


@router.post("/complete", response_model=PaymentCompleteRes)
def complete_payment(req: PaymentCompleteReq, db: Session = Depends(get_db)):
    payment = db.get(Payment, req.payment_id)
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment order not found")

    course = db.get(Course, payment.course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if payment.status == "PAID":
        return PaymentCompleteRes(
            payment_id=payment.payment_id,
            course_id=payment.course_id,
            course_title=payment.order_name,
            status=payment.status,
        )

    if not settings.PORTONE_API_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment verification is not configured",
        )

    url = f"https://api.portone.io/payments/{quote(payment.payment_id, safe='')}"
    request = UrlRequest(url, headers={"Authorization": f"PortOne {settings.PORTONE_API_SECRET}"}, method="GET")
    try:
        with urlopen(request, timeout=10) as response:
            portone_payment = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not verify the payment with PortOne",
        ) from exc
    except (URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not verify the payment with PortOne",
        ) from exc

    amount = portone_payment.get("amount") or {}
    if portone_payment.get("status") != "PAID":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment is not completed")
    if portone_payment.get("id") != payment.payment_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment ID does not match")
    if amount.get("total") != payment.amount or portone_payment.get("currency") != "KRW":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment amount does not match the order")
    if portone_payment.get("orderName") != payment.order_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment order does not match")

    payment.status = "PAID"
    payment.transaction_id = portone_payment.get("transactionId")
    payment.paid_at = datetime.now(timezone.utc)
    db.commit()
    return PaymentCompleteRes(
        payment_id=payment.payment_id,
        course_id=payment.course_id,
        course_title=payment.order_name,
        status=payment.status,
    )