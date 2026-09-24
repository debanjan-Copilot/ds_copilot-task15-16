from typing import Any, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

Entity = TypeVar("Entity")


class BaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def commit(self) -> None:
        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def refresh(self, entity: Entity) -> Entity:
        self.db.refresh(entity)
        return entity

    def save(self, entity: Entity) -> Entity:
        try:
            self.db.add(entity)
            self.commit()
            return self.refresh(entity)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, entity: Any) -> None:
        self.db.delete(entity)
        self.commit()
