from flask import Blueprint, render_template, request

from models import laporan as laporan_model
from models import simpang as simpang_model

bp = Blueprint("laporan", __name__, url_prefix="/laporan")


@bp.route("")
def index():
    tanggal_mulai = request.args.get("tanggal_mulai", "").strip()
    tanggal_selesai = request.args.get("tanggal_selesai", "").strip()
    id_simpang = request.args.get("id_simpang", "").strip()
    kategori = request.args.get("kategori", "").strip()

    laporan = laporan_model.get_laporan_aduan(
        tanggal_mulai, tanggal_selesai, id_simpang, kategori
    )

    return render_template(
        "laporan/aduan.html",
        laporan=laporan,
        simpang=simpang_model.get_dropdown_list(),
        kategori_gangguan=laporan_model.get_kategori_gangguan_list(),
        tanggal_mulai=tanggal_mulai,
        tanggal_selesai=tanggal_selesai,
        id_simpang=id_simpang,
        kategori=kategori,
    )
