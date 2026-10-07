import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        os.makedirs(self.upload_dir, exist_ok=True)
        self.firebase_initialized = False
        
        # Initialize Firebase Admin if credentials are provided
        if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            try:
                import firebase_admin
                from firebase_admin import credentials, storage
                if not firebase_admin._apps:
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    firebase_admin.initialize_app(cred, {
                        'storageBucket': settings.FIREBASE_STORAGE_BUCKET
                    })
                self.firebase_initialized = True
            except Exception as e:
                print(f"⚠️ Firebase initialization warning: {e}. Falling back to local storage.")

    async def save_file(self, file: UploadFile, subfolder: str = "meals") -> str:
        """Saves file to Firebase Storage if available, otherwise to local media directory."""
        folder_path = self.upload_dir / subfolder
        os.makedirs(folder_path, exist_ok=True)

        ext = Path(file.filename).suffix if file.filename else ".jpg"
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = folder_path / unique_filename

        # Save locally first
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        await file.seek(0)

        # Upload to Firebase if initialized
        if self.firebase_initialized and settings.FIREBASE_STORAGE_BUCKET:
            try:
                from firebase_admin import storage
                bucket = storage.bucket()
                blob_path = f"{subfolder}/{unique_filename}"
                blob = bucket.blob(blob_path)
                blob.upload_from_filename(str(file_path), content_type=file.content_type)
                blob.make_public()
                return blob.public_url
            except Exception as e:
                print(f"⚠️ Firebase Upload Failed: {e}. Returning local relative path.")

        # Fallback to local static file URL route
        return f"/uploads/{subfolder}/{unique_filename}"

storage_service = StorageService()
