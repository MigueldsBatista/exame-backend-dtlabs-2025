from sqlalchemy.orm import Session
from typing import Generic, Type, TypeVar
from sqlalchemy.exc import NoReferencedTableError
from sqlalchemy.exc import IntegrityError

T = TypeVar("T")

class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], db: Session):
        """Initialize the repository with a model and a database session."""
        self.model = model
        self.db = db

    def find_all(self):
        return self.db.query(self.model).all()

    def find_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def delete(self, id: int):
        obj = self.find_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

    def save(self, obj: T):
        if obj is None:
            raise ValueError("Object can't be None")
        
        try:
            existing_obj = self.find_by_id(obj.id)
            if existing_obj:
                for key, value in existing_obj.__dict__.items():
                    if key != "_sa_instance_state":
                        setattr(existing_obj, key, value)
                self.db.commit()
                return existing_obj
            
            self.db.add(obj)
            self.db.commit()
            return obj
        except (NoReferencedTableError, IntegrityError) as e:
            self.db.rollback()
            raise e
