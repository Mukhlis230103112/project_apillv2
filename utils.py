import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def save_uploaded_photo(file_storage, prefix=""):
    """
    Menyimpan file foto yang diupload dengan nama acak (UUID) supaya
    tidak bentrok antar file, lalu mengembalikan path relatif
    (untuk disimpan di database) atau None kalau tidak ada file.

    Melempar ValueError kalau ekstensi file tidak diperbolehkan.
    """
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_file(file_storage.filename):
        raise ValueError(
            "Format file tidak diperbolehkan. "
            "Gunakan JPG, JPEG, PNG, atau WEBP."
        )

    original_name = secure_filename(file_storage.filename)
    extension = original_name.rsplit(".", 1)[1].lower()
    new_name = f"{prefix}{uuid.uuid4().hex}.{extension}"

    file_storage.save(
        os.path.join(current_app.config["UPLOAD_FOLDER"], new_name)
    )

    return f"uploads/aduan/{new_name}"
