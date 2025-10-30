# app/sync_data.py
import os
import requests
from app.cloudinary_utils import upload_to_cloudinary
from app.drive_importer import get_drive_service, get_file_download_url
from app.database import SessionLocal
from app.model import Image
from dotenv import load_dotenv
import threading

load_dotenv()

# Global stop flag
_stop_sync = threading.Event()

def stop_sync():
    """Stop the current sync operation."""
    _stop_sync.set()

def reset_stop_flag():
    """Reset the stop flag before starting a new sync."""
    _stop_sync.clear()

def sync_images_from_drive(folder_id: str):
    print(f"🔍 Starting Google Drive → Cloudinary sync for folder {folder_id}")
    reset_stop_flag()

    service = get_drive_service()
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])

    print(f"📁 Found {len(files)} images in the folder.")

    db = SessionLocal()
    os.makedirs("downloads", exist_ok=True)

    for file in files:
        if _stop_sync.is_set():
            print("🛑 Sync stopped by user.")
            break

        file_id = file["id"]
        file_name = file["name"]

        print(f"⬇️ Downloading {file_name} from Google Drive...")
        try:
            download_url = get_file_download_url(file_id)
            if not download_url:
                print(f"⚠️ Skipping {file_name}, no download URL.")
                continue

            response = requests.get(download_url)
            if response.status_code != 200:
                print(f"⚠️ Failed to download {file_name}")
                continue

            temp_path = os.path.join("downloads", file_name)
            with open(temp_path, "wb") as f:
                f.write(response.content)

            print(f"☁️ Uploading {file_name} to Cloudinary...")
            cloud_url = upload_to_cloudinary(temp_path)
            if cloud_url:
                print(f"✅ Uploaded: {cloud_url}")
                new_image = Image(filename=file_name, cloudinary_url=cloud_url)
                db.add(new_image)
                db.commit()

            os.remove(temp_path)
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

    db.close()
    print("🎯 Sync completed and data stored in PostgreSQL")
