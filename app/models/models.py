from datetime import datetime

from sqlmodel import Field, SQLModel


class TestModel(SQLModel):  # table=True to make it a db table
    id: int | None = Field(default=None, primary_key=True)
    name: str
    date_created: datetime
