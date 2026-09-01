from db import db_cursor


def get_all():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                p.id_perangkat, p.id_simpang, s.kode_simpang, s.nama_simpang,
                p.jenis_perangkat, p.jenis_ukuran, p.daya, p.sistem,
                p.komunikasi, p.jumlah, p.kondisi, p.kategori_kondisi,
                p.keterangan
            FROM perangkat p
            JOIN simpang s ON s.id_simpang = p.id_simpang
            ORDER BY p.id_perangkat;
        """)
        return cursor.fetchall()


def get_by_id(id_perangkat):
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                p.id_perangkat, p.id_simpang, s.kode_simpang, s.nama_simpang,
                p.jenis_perangkat, p.jenis_ukuran, p.daya, p.sistem,
                p.komunikasi, p.jumlah, p.kondisi, p.kategori_kondisi,
                p.keterangan
            FROM perangkat p
            JOIN simpang s ON s.id_simpang = p.id_simpang
            WHERE p.id_perangkat = %s;
        """, (id_perangkat,))
        return cursor.fetchone()


def get_for_edit(id_perangkat):
    """Data mentah (tanpa join) untuk mengisi form edit."""
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                id_perangkat, id_simpang, jenis_perangkat, jenis_ukuran,
                daya, sistem, komunikasi, jumlah, kondisi, keterangan
            FROM perangkat
            WHERE id_perangkat = %s;
        """, (id_perangkat,))
        return cursor.fetchone()


def get_dropdown_list():
    """Daftar perangkat (dengan info simpang) untuk dropdown form monitoring."""
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                p.id_perangkat, s.kode_simpang, s.nama_simpang,
                p.jenis_perangkat, p.jenis_ukuran
            FROM perangkat p
            JOIN simpang s ON s.id_simpang = p.id_simpang
            ORDER BY s.nama_simpang, p.jenis_perangkat;
        """)
        return cursor.fetchall()


def create(data):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO perangkat (
                id_simpang, jenis_perangkat, jenis_ukuran, daya,
                sistem, komunikasi, jumlah, kondisi, keterangan
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            data["id_simpang"],
            data["jenis_perangkat"],
            data["jenis_ukuran"] or None,
            data["daya"] or None,
            data["sistem"] or None,
            data["komunikasi"] or None,
            int(data["jumlah"]) if data["jumlah"] else None,
            data["kondisi"] or None,
            data["keterangan"] or None,
        ))


def update(id_perangkat, data):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            UPDATE perangkat
            SET
                id_simpang = %s, jenis_perangkat = %s, jenis_ukuran = %s,
                daya = %s, sistem = %s, komunikasi = %s, jumlah = %s,
                kondisi = %s, keterangan = %s
            WHERE id_perangkat = %s;
        """, (
            data["id_simpang"],
            data["jenis_perangkat"],
            data["jenis_ukuran"] or None,
            data["daya"] or None,
            data["sistem"] or None,
            data["komunikasi"] or None,
            int(data["jumlah"]) if data["jumlah"] else None,
            data["kondisi"] or None,
            data["keterangan"] or None,
            id_perangkat,
        ))


def delete(id_perangkat):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            DELETE FROM perangkat WHERE id_perangkat = %s;
        """, (id_perangkat,))
