from flask import Blueprint, redirect, render_template, request, url_for

from models import monitoring as monitoring_model
from models import perangkat as perangkat_model

bp = Blueprint("monitoring", __name__, url_prefix="/monitoring")

_FORM_FIELDS = [
    "id_perangkat", "tanggal_pemeriksaan", "kondisi",
    "status", "keterangan", "petugas",
]


def _read_form():
    return {field: request.form.get(field, "").strip() for field in _FORM_FIELDS}


@bp.route("")
def index():
    return render_template(
        "monitoring/index.html", monitoring=monitoring_model.get_all()
    )


@bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        try:
            monitoring_model.create(_read_form())
        except Exception as e:
            return f"Terjadi error: {e}", 500
        return redirect(url_for("monitoring.index"))

    return render_template(
        "monitoring/form.html",
        perangkat=perangkat_model.get_dropdown_list(),
        edit=False,
        data=None,
    )


@bp.route("/edit/<int:id_monitoring>", methods=["GET", "POST"])
def edit(id_monitoring):
    if request.method == "POST":
        try:
            monitoring_model.update(id_monitoring, _read_form())
        except Exception as e:
            return f"Terjadi error: {e}", 500
        return redirect(url_for("monitoring.index"))

    data = monitoring_model.get_by_id(id_monitoring)
    if data is None:
        return "Data monitoring tidak ditemukan", 404

    return render_template(
        "monitoring/form.html",
        data=data,
        perangkat=perangkat_model.get_dropdown_list(),
        edit=True,
    )


@bp.route("/hapus/<int:id_monitoring>", methods=["POST"])
def hapus(id_monitoring):
    try:
        monitoring_model.delete(id_monitoring)
    except Exception as e:
        return f"Error hapus monitoring: {e}", 500
    return redirect(url_for("monitoring.index"))
