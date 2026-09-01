import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Konfigurasi aplikasi, diambil dari environment variable (.env)."""

    # Keamanan
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-ubah-di-production")

    # Mode debug: aktif hanya kalau FLASK_DEBUG=True di .env
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Database PostgreSQL
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Upload foto aduan
    UPLOAD_FOLDER = os.path.join("static", "uploads", "aduan")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Batas ukuran upload (10 MB) supaya server tidak kebanjiran file besar
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
