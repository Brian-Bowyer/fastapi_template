from datetime import datetime

from sqlmodel import Field, SQLModel


class TestModelBase(SQLModel):
    name: str
    date_created: datetime


class TestModel(TestModelBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
