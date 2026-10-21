from pydantic import BaseModel, Field


class PaymentPrepareReq(BaseModel):
    course_id: int = Field(gt=0)


class PaymentPrepareRes(BaseModel):
    payment_id: str
    order_name: str
    total_amount: int


class PaymentCompleteReq(BaseModel):
    payment_id: str = Field(min_length=6, max_length=64)


class PaymentCompleteRes(BaseModel):
    payment_id: str
    course_id: int
    course_title: str
    status: str