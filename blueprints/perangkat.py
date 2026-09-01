from flask import Blueprint, redirect, render_template, request, url_for

from models import perangkat as perangkat_model
from models import simpang as simpang_model

bp = Blueprint("perangkat", __name__, url_prefix="/perangkat")

_FORM_FIELDS = [
    "id_simpang", "jenis_perangkat", "jenis_ukuran", "daya", "sistem",
    "komunikasi", "jumlah", "kondisi", "keterangan",
]


def _read_form():
    return {field: request.form.get(field, "").strip() for field in _FORM_FIELDS}


@bp.route("")
def index():
    return render_template(
        "perangkat/index.html", perangkat=perangkat_model.get_all()
    )


@bp.route("/detail/<int:id_perangkat>")
def detail(id_perangkat):
    data = perangkat_model.get_by_id(id_perangkat)
    if data is None:
        return "Data perangkat tidak ditemukan", 404
    return render_template("perangkat/detail.html", data=data)


@bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        try:
            perangkat_model.create(_read_form())
        except Exception as e:
            return f"Terjadi error: {e}", 500
        return redirect(url_for("perangkat.index"))

    return render_template(
        "perangkat/form.html",
        simpang=simpang_model.get_dropdown_list(),
        edit=False,
        data=None,
    )


@bp.route("/edit/<int:id_perangkat>", methods=["GET", "POST"])
def edit(id_perangkat):
    if request.method == "POST":
        try:
            perangkat_model.update(id_perangkat, _read_form())
        except Exception as e:
            return f"Terjadi error: {e}", 500
        return redirect(url_for("perangkat.detail", id_perangkat=id_perangkat))

    data = perangkat_model.get_for_edit(id_perangkat)
    if data is None:
        return "Data perangkat tidak ditemukan", 404

    return render_template(
        "perangkat/form.html",
        data=data,
        simpang=simpang_model.get_dropdown_list(),
        edit=True,
    )


@bp.route("/hapus/<int:id_perangkat>", methods=["POST"])
def hapus(id_perangkat):
    try:
        perangkat_model.delete(id_perangkat)
    except Exception as e:
        return f"Error hapus perangkat: {e}", 500
    return redirect(url_for("perangkat.index"))
