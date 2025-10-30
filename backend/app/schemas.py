from pydantic import BaseModel, ConfigDict

class ImageBase(BaseModel):
    filename: str
    cloudinary_url: str

class ImageCreate(ImageBase):
    pass

class ImageOut(ImageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
