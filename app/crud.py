from sqlalchemy.orm import Session

from . import models

def get_sepsis(db: Session):
    return db.query(models.sepsis.authors, models.sepsis.year, models.sepsis.journal).all()
