from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from app.models import TestModel, TestModelBase
from app.utils.errors import NotFoundError


def create(model: TestModelBase, db: Session = Depends(get_session)) -> TestModel:
    db_model = TestModel.model_validate(model)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def read(model_id: int, db: Session = Depends(get_session)) -> TestModel:
    model = db.get(TestModel, model_id)
    if not model:
        raise NotFoundError(f"TestModel {model_id} could not be found")
    return model


def update(
    model_id: int, model: TestModelBase, db: Session = Depends(get_session)
) -> TestModel:
    model_to_update = read(model_id, db)

    update_data = model.model_dump(exclude_unset=True)
    model_to_update.sqlmodel_update(update_data)

    db.add(model_to_update)
    db.commit()
    db.refresh(model_to_update)
    return model_to_update


def delete(model_id: int, db: Session = Depends(get_session)) -> dict[str, bool]:
    model_to_delete = read(model_id, db)
    db.delete(model_to_delete)
    db.commit()
    return {"success": True}
