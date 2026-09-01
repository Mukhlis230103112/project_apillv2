from db import db_cursor

_KOLOM_SIMPANG = """
    id_simpang,
    kode_simpang,
    nama_simpang,
    jenis_simpang,
    sumber_daya,
    sistem,
    aset,
    kewenangan,
    status_jalan,
    ruas_jalan,
    tahun_anggaran,
    latitude,
    longitude,
    wilayah
"""


def get_all():
    with db_cursor() as cursor:
        cursor.execute(f"""
            SELECT {_KOLOM_SIMPANG}
            FROM simpang
            ORDER BY id_simpang;
        """)
        return cursor.fetchall()


def get_by_id(id_simpang):
    with db_cursor() as cursor:
        cursor.execute(f"""
            SELECT {_KOLOM_SIMPANG}
            FROM simpang
            WHERE id_simpang = %s;
        """, (id_simpang,))
        return cursor.fetchone()


def get_dropdown_list():
    """Daftar ringkas (id, kode, nama) untuk dropdown di form lain."""
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT id_simpang, kode_simpang, nama_simpang
            FROM simpang
            ORDER BY nama_simpang;
        """)
        return cursor.fetchall()


def create(data):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO simpang (
                kode_simpang, nama_simpang, jenis_simpang, wilayah,
                sumber_daya, sistem, aset, kewenangan, status_jalan,
                ruas_jalan, tahun_anggaran, latitude, longitude
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            );
        """, (
            data["kode_simpang"],
            data["nama_simpang"],
            data["jenis_simpang"],
            data["wilayah"] or None,
            data["sumber_daya"],
            data["sistem"],
            data["aset"],
            data["kewenangan"],
            data["status_jalan"],
            data["ruas_jalan"],
            data["tahun_anggaran"] or None,
            data["latitude"] or None,
            data["longitude"] or None,
        ))


def update(id_simpang, data):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            UPDATE simpang
            SET
                kode_simpang = %s, nama_simpang = %s, jenis_simpang = %s,
                wilayah = %s, sumber_daya = %s, sistem = %s, aset = %s,
                kewenangan = %s, status_jalan = %s, ruas_jalan = %s,
                tahun_anggaran = %s, latitude = %s, longitude = %s
            WHERE id_simpang = %s;
        """, (
            data["kode_simpang"],
            data["nama_simpang"],
            data["jenis_simpang"],
            data["wilayah"] or None,
            data["sumber_daya"],
            data["sistem"],
            data["aset"],
            data["kewenangan"],
            data["status_jalan"],
            data["ruas_jalan"],
            data["tahun_anggaran"] or None,
            data["latitude"] or None,
            data["longitude"] or None,
            id_simpang,
        ))


def delete(id_simpang):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            DELETE FROM simpang WHERE id_simpang = %s;
        """, (id_simpang,))


def get_geojson_rows():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                id_simpang, kode_simpang, nama_simpang,
                jenis_simpang, wilayah, latitude, longitude
            FROM simpang
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
        """)
        return cursor.fetchall()
