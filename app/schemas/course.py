from pydantic import BaseModel, ConfigDict


class CourseListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    instructor_name: str
    price: int
    category: str
    level: str
    thumbnail_url: str | None
    summary: str


class CourseDetail(CourseListItem):
    description: str
