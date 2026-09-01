import os

from db import db_cursor


def get_all():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                a.id_aduan, a.tanggal_aduan, s.kode_simpang, s.nama_simpang,
                a.lokasi_simpang, a.jenis_gangguan, a.kategori_gangguan,
                a.pelapor, a.status_aduan
            FROM aduan a
            JOIN simpang s ON s.id_simpang = a.id_simpang
            ORDER BY a.tanggal_aduan DESC, a.id_aduan DESC;
        """)
        return cursor.fetchall()


def get_detail(id_aduan):
    """Data aduan digabung dengan status penanganannya (kalau ada)."""
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                a.id_aduan, a.tanggal_aduan, s.kode_simpang, s.nama_simpang,
                a.lokasi_simpang, a.detail_posisi, a.jenis_gangguan,
                a.kategori_gangguan, a.penyebab_gangguan, a.pelapor,
                a.foto_kondisi_awal, a.status_aduan,
                p.id_penanganan, p.status_penanganan, p.tindak_lanjut,
                p.pic, p.waktu_tl, p.foto_proses_tl, p.foto_kondisi_akhir
            FROM aduan a
            JOIN simpang s ON s.id_simpang = a.id_simpang
            LEFT JOIN penanganan p ON p.id_aduan = a.id_aduan
            WHERE a.id_aduan = %s;
        """, (id_aduan,))
        return cursor.fetchone()


def get_for_edit(id_aduan):
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                id_aduan, id_simpang, tanggal_aduan, lokasi_simpang,
                detail_posisi, jenis_gangguan, penyebab_gangguan, pelapor,
                foto_kondisi_awal, status_aduan
            FROM aduan
            WHERE id_aduan = %s;
        """, (id_aduan,))
        return cursor.fetchone()


def create(data, foto_kondisi_awal):
    """Membuat aduan baru sekaligus baris penanganan kosong. Return id_aduan."""
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO aduan (
                id_simpang, tanggal_aduan, lokasi_simpang, detail_posisi,
                jenis_gangguan, penyebab_gangguan, pelapor,
                foto_kondisi_awal, status_aduan
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_aduan;
        """, (
            data["id_simpang"],
            data["tanggal_aduan"],
            data["lokasi_simpang"] or None,
            data["detail_posisi"] or None,
            data["jenis_gangguan"] or None,
            data["penyebab_gangguan"] or None,
            data["pelapor"] or None,
            foto_kondisi_awal,
            "Baru",
        ))
        id_aduan = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO penanganan (id_aduan, status_penanganan)
            VALUES (%s, %s);
        """, (id_aduan, "Diproses"))

        return id_aduan


def update(id_aduan, data, foto_baru):
    with db_cursor(commit=True) as cursor:
        if foto_baru:
            cursor.execute("""
                UPDATE aduan
                SET
                    id_simpang = %s, tanggal_aduan = %s, lokasi_simpang = %s,
                    detail_posisi = %s, jenis_gangguan = %s,
                    penyebab_gangguan = %s, pelapor = %s,
                    foto_kondisi_awal = %s
                WHERE id_aduan = %s;
            """, (
                data["id_simpang"], data["tanggal_aduan"],
                data["lokasi_simpang"] or None, data["detail_posisi"] or None,
                data["jenis_gangguan"] or None, data["penyebab_gangguan"] or None,
                data["pelapor"] or None, foto_baru, id_aduan,
            ))
        else:
            cursor.execute("""
                UPDATE aduan
                SET
                    id_simpang = %s, tanggal_aduan = %s, lokasi_simpang = %s,
                    detail_posisi = %s, jenis_gangguan = %s,
                    penyebab_gangguan = %s, pelapor = %s
                WHERE id_aduan = %s;
            """, (
                data["id_simpang"], data["tanggal_aduan"],
                data["lokasi_simpang"] or None, data["detail_posisi"] or None,
                data["jenis_gangguan"] or None, data["penyebab_gangguan"] or None,
                data["pelapor"] or None, id_aduan,
            ))


def update_penanganan(id_aduan, tindak_lanjut, pic, waktu_tl,
                       foto_proses_tl=None, foto_kondisi_akhir=None):
    """
    Update data penanganan. Status otomatis jadi 'Selesai' kalau foto
    kondisi akhir sudah ada, atau 'Diproses' kalau baru foto proses saja.
    """
    tindak_lanjut = tindak_lanjut or None
    pic = pic or None
    waktu_tl = waktu_tl or None

    with db_cursor(commit=True) as cursor:
        if foto_proses_tl and foto_kondisi_akhir:
            cursor.execute("""
                UPDATE penanganan
                SET tindak_lanjut = %s, pic = %s, waktu_tl = %s,
                    foto_proses_tl = %s, foto_kondisi_akhir = %s,
                    status_penanganan = 'Selesai'
                WHERE id_aduan = %s;
            """, (tindak_lanjut, pic, waktu_tl,
                  foto_proses_tl, foto_kondisi_akhir, id_aduan))

        elif foto_proses_tl:
            cursor.execute("""
                UPDATE penanganan
                SET tindak_lanjut = %s, pic = %s, waktu_tl = %s,
                    foto_proses_tl = %s, status_penanganan = 'Diproses'
                WHERE id_aduan = %s;
            """, (tindak_lanjut, pic, waktu_tl, foto_proses_tl, id_aduan))

        elif foto_kondisi_akhir:
            cursor.execute("""
                UPDATE penanganan
                SET tindak_lanjut = %s, pic = %s, waktu_tl = %s,
                    foto_kondisi_akhir = %s, status_penanganan = 'Selesai'
                WHERE id_aduan = %s;
            """, (tindak_lanjut, pic, waktu_tl, foto_kondisi_akhir, id_aduan))

        else:
            cursor.execute("""
                UPDATE penanganan
                SET tindak_lanjut = %s, pic = %s, waktu_tl = %s
                WHERE id_aduan = %s;
            """, (tindak_lanjut, pic, waktu_tl, id_aduan))


def delete(id_aduan):
    """Hapus aduan beserta file foto terkait (kondisi awal, proses, akhir)."""
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            SELECT a.foto_kondisi_awal, p.foto_proses_tl, p.foto_kondisi_akhir
            FROM aduan a
            LEFT JOIN penanganan p ON p.id_aduan = a.id_aduan
            WHERE a.id_aduan = %s;
        """, (id_aduan,))
        foto = cursor.fetchone()

        cursor.execute("""
            DELETE FROM aduan WHERE id_aduan = %s;
        """, (id_aduan,))

    if foto:
        for path in foto:
            if not path:
                continue
            full_path = os.path.join("static", path)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except OSError:
                    pass
