import cloudinary
import cloudinary.uploader

from app.core.config import get_settings

settings = get_settings()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_profile_picture(file_bytes: bytes, student_id: int) -> str:
    """Uploads to Cloudinary, returns the resulting HTTPS URL."""
    result = cloudinary.uploader.upload(
        file_bytes,
        folder="student_progress_tracker/profile_pictures",
        public_id=f"student_{student_id}",
        overwrite=True,
        transformation=[{"width": 400, "height": 400, "crop": "fill", "gravity": "face"}],
    )
    return result["secure_url"]