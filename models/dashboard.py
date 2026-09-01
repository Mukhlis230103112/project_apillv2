from db import db_cursor

NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def get_ringkasan():
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM dashboard_ringkasan;")
        return cursor.fetchone()


def get_kondisi_perangkat():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT kategori_kondisi, jumlah
            FROM dashboard_kondisi_perangkat;
        """)
        return cursor.fetchall()


def get_kategori_gangguan():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT kategori_gangguan, jumlah
            FROM dashboard_kategori_gangguan;
        """)
        return cursor.fetchall()


def get_aduan_per_simpang():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT kode_simpang, nama_simpang, jumlah_aduan
            FROM dashboard_aduan_simpang
            WHERE jumlah_aduan > 0
            ORDER BY jumlah_aduan DESC;
        """)
        return cursor.fetchall()


def get_aduan_bulanan():
    """
    Return (rows_asli, label_bulan, jumlah_per_bulan) siap pakai
    untuk chart bulanan di dashboard.
    """
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT bulan, jumlah_aduan
            FROM dashboard_aduan_bulanan
            ORDER BY bulan;
        """)
        rows = cursor.fetchall()

    labels = [NAMA_BULAN[item[0] - 1] for item in rows]
    jumlah = [item[1] for item in rows]

    return rows, labels, jumlah
