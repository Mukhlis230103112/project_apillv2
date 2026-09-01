from flask import Blueprint, redirect, render_template, request, url_for

from models import simpang as simpang_model

bp = Blueprint("simpang", __name__, url_prefix="/simpang")

_FORM_FIELDS = [
    "kode_simpang", "nama_simpang", "jenis_simpang", "wilayah",
    "sumber_daya", "sistem", "aset", "kewenangan", "status_jalan",
    "ruas_jalan", "tahun_anggaran", "latitude", "longitude",
]


def _read_form():
    return {field: request.form[field] for field in _FORM_FIELDS}


@bp.route("")
def index():
    return render_template("simpang/index.html", simpang=simpang_model.get_all())


@bp.route("/detail/<int:id_simpang>")
def detail(id_simpang):
    data = simpang_model.get_by_id(id_simpang)
    if data is None:
        return "Data simpang tidak ditemukan", 404
    return render_template("simpang/detail.html", data=data)


@bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        try:
            simpang_model.create(_read_form())
        except Exception as e:
            return f"Terjadi error: {e}", 500
        return redirect(url_for("simpang.index"))

    return render_template("simpang/form.html")


@bp.route("/edit/<int:id_simpang>", methods=["GET", "POST"])
def edit(id_simpang):
    if request.method == "POST":
        try:
            simpang_model.update(id_simpang, _read_form())
        except Exception as e:
            return f"Terjadi error: {e}", 500
        return redirect(url_for("simpang.detail", id_simpang=id_simpang))

    data = simpang_model.get_by_id(id_simpang)
    if data is None:
        return "Data simpang tidak ditemukan", 404
    return render_template("simpang/form.html", data=data, edit=True)


@bp.route("/hapus/<int:id_simpang>", methods=["POST"])
def hapus(id_simpang):
    try:
        simpang_model.delete(id_simpang)
    except Exception as e:
        return f"Terjadi error: {e}", 500
    return redirect(url_for("simpang.index"))
