from contextlib import contextmanager

import psycopg2
from flask import current_app


def get_connection():
    """Membuka satu koneksi baru ke database PostgreSQL."""
    return psycopg2.connect(
        host=current_app.config["DB_HOST"],
        port=current_app.config["DB_PORT"],
        database=current_app.config["DB_NAME"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
    )


@contextmanager
def db_cursor(commit=False):
    """
    Context manager untuk satu transaksi database.

    Menggantikan pola manual:
        conn = get_connection()
        cursor = conn.cursor()
        ...
        cursor.close()
        conn.close()

    yang sebelumnya diulang di setiap route.

    Pemakaian untuk query baca (SELECT):
        with db_cursor() as cursor:
            cursor.execute("SELECT ...")
            data = cursor.fetchall()

    Pemakaian untuk query tulis (INSERT/UPDATE/DELETE),
    otomatis commit jika sukses dan rollback jika terjadi error:
        with db_cursor(commit=True) as cursor:
            cursor.execute("INSERT ...")

    Cursor dan koneksi selalu ditutup di akhir (baik sukses maupun error),
    jadi tidak ada lagi risiko koneksi yang tidak tertutup.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        if commit:
            conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
