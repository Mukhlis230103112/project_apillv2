from db import db_cursor


def get_all():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                m.id_monitoring, m.id_perangkat, s.kode_simpang,
                s.nama_simpang, p.jenis_perangkat, m.tanggal_pemeriksaan,
                m.kondisi, m.status, m.keterangan, m.petugas
            FROM monitoring m
            JOIN perangkat p ON p.id_perangkat = m.id_perangkat
            JOIN simpang s ON s.id_simpang = p.id_simpang
            ORDER BY m.tanggal_pemeriksaan DESC, m.id_monitoring DESC;
        """)
        return cursor.fetchall()


def get_by_id(id_monitoring):
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT
                id_monitoring, id_perangkat, tanggal_pemeriksaan,
                kondisi, status, keterangan, petugas
            FROM monitoring
            WHERE id_monitoring = %s;
        """, (id_monitoring,))
        return cursor.fetchone()


def create(data):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            INSERT INTO monitoring (
                id_perangkat, tanggal_pemeriksaan, kondisi,
                status, keterangan, petugas
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            data["id_perangkat"],
            data["tanggal_pemeriksaan"],
            data["kondisi"],
            data["status"],
            data["keterangan"] or None,
            data["petugas"] or None,
        ))


def update(id_monitoring, data):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            UPDATE monitoring
            SET
                id_perangkat = %s, tanggal_pemeriksaan = %s, kondisi = %s,
                status = %s, keterangan = %s, petugas = %s
            WHERE id_monitoring = %s;
        """, (
            data["id_perangkat"],
            data["tanggal_pemeriksaan"],
            data["kondisi"],
            data["status"],
            data["keterangan"] or None,
            data["petugas"] or None,
            id_monitoring,
        ))


def delete(id_monitoring):
    with db_cursor(commit=True) as cursor:
        cursor.execute("""
            DELETE FROM monitoring WHERE id_monitoring = %s;
        """, (id_monitoring,))
