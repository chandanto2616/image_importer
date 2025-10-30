
from sqlalchemy.orm import Session
from . import model, schemas

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = model.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Image).offset(skip).limit(limit).all()
