from flask import Blueprint, render_template

from models import dashboard as dashboard_model

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    ringkasan = dashboard_model.get_ringkasan()
    kondisi_perangkat = dashboard_model.get_kondisi_perangkat()
    kategori_gangguan = dashboard_model.get_kategori_gangguan()
    aduan_simpang = dashboard_model.get_aduan_per_simpang()
    aduan_bulanan, bulan_labels, bulan_data = dashboard_model.get_aduan_bulanan()

    return render_template(
        "dashboard.html",
        ringkasan=ringkasan,
        kondisi_perangkat=kondisi_perangkat,
        kategori_gangguan=kategori_gangguan,
        aduan_simpang=aduan_simpang,
        aduan_bulanan=aduan_bulanan,
        bulan_labels=bulan_labels,
        bulan_data=bulan_data,
    )
