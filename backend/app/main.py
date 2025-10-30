# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal, Base, engine
from app.model import Image
from app.sync_data import sync_images_from_drive, stop_sync
import threading
import os
import re

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Initialize app
app = FastAPI(title="Image Importer API")

# ✅ Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Frontend mount (if static files exist)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
print("📁 Frontend path:", frontend_path)
if os.path.isdir(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>Image Importer API</h1><p>Use /images to see stored images.</p>")


# ✅ Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Get all images
@app.get("/images")
def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return [
        {"id": i.id, "filename": i.filename, "cloudinary_url": i.cloudinary_url}
        for i in images
    ]


# ✅ Start sync
@app.post("/start-sync")
def start_sync(body: dict):
    folder_url = body.get("folder_url") or body.get("folder_id")
    if not folder_url:
        raise HTTPException(status_code=400, detail="folder_url or folder_id required")

    # Extract folder ID if it's a full Google Drive URL
    match = re.search(r"/folders/([a-zA-Z0-9_-]+)", folder_url)
    folder_id = match.group(1) if match else folder_url.strip()

    # Clear existing images before sync
    db = SessionLocal()
    db.query(Image).delete()
    db.commit()
    db.close()

    # Start sync in background thread
    thread = threading.Thread(target=sync_images_from_drive, args=(folder_id,))
    thread.start()

    return {"status": "started", "folder_id": folder_id}


# ✅ Clear all images manually (optional)
@app.post("/clear-images")
def clear_images(db: Session = Depends(get_db)):
    db.query(Image).delete()
    db.commit()
    return {"message": "All images cleared successfully."}


# ✅ Stop sync process
@app.post("/stop-sync")
def stop_sync_api():
    stop_sync()
    return {"message": "Sync stopped successfully."}
