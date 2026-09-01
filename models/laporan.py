from db import db_cursor


def get_laporan_aduan(tanggal_mulai, tanggal_selesai, id_simpang, kategori):
    query = """
        SELECT
            id_aduan,
            "Tanggal Aduan",
            "Nama Simpang",
            "Lokasi Simpang",
            "Detail Posisi",
            "Jenis Gangguan",
            "Kategori Gangguan",
            "Penyebab Gangguan",
            "Pelapor",
            "Tindak Lanjut",
            "PIC",
            "Waktu TL",
            "Kondisi Awal",
            "Proses TL",
            "Kondisi Akhir"
        FROM laporan_aduan
        WHERE 1 = 1
    """
    params = []

    if tanggal_mulai:
        query += ' AND "Tanggal Aduan"::date >= %s'
        params.append(tanggal_mulai)

    if tanggal_selesai:
        query += ' AND "Tanggal Aduan"::date <= %s'
        params.append(tanggal_selesai)

    if id_simpang:
        query += """
            AND id_aduan IN (
                SELECT a.id_aduan FROM aduan a WHERE a.id_simpang = %s
            )
        """
        params.append(id_simpang)

    if kategori:
        query += ' AND "Kategori Gangguan" = %s'
        params.append(kategori)

    query += ' ORDER BY "Tanggal Aduan" DESC, id_aduan DESC'

    with db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def get_kategori_gangguan_list():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT kategori_gangguan
            FROM aduan
            WHERE kategori_gangguan IS NOT NULL
              AND TRIM(kategori_gangguan) <> ''
            ORDER BY kategori_gangguan;
        """)
        return cursor.fetchall()
