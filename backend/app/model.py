from sqlalchemy import Column, Integer, String
from app.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    cloudinary_url = Column(String, nullable=False)
