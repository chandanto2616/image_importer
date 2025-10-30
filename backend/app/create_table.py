from app.database import Base, engine
from app.model import Image


print("✅ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
