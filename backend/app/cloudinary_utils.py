import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv()

# ✅ Initialize Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_to_cloudinary(file_path: str):
    try:
        print("✅ Using CLOUDINARY_URL from .env")
        result = cloudinary.uploader.upload(file_path)
        return result.get("secure_url")
    except Exception as e:
        print(f"❌ Cloudinary upload failed: {e}")
        return None
