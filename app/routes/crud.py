from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.controllers import create, delete, read, update
from app.database import get_session
from app.models import TestModel, TestModelBase

router = APIRouter()


@router.post("/")
def create_model(model: TestModelBase, db: Session = Depends(get_session)) -> TestModel:
    return create(model, db=db)


@router.get("/{model_id}")
def read_model(model_id: int, db: Session = Depends(get_session)) -> TestModel:
    return read(model_id, db=db)


# patch requires a separate update model
@router.put("/{model_id}")
def update_model(
    model_id: int, model: TestModelBase, db: Session = Depends(get_session)
) -> TestModel:
    return update(model_id, model, db=db)


@router.delete("/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_session)) -> dict[str, bool]:
    return delete(model_id, db=db)
