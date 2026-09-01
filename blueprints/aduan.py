from flask import Blueprint, redirect, render_template, request, url_for

from models import aduan as aduan_model
from models import simpang as simpang_model
from utils import save_uploaded_photo

bp = Blueprint("aduan", __name__, url_prefix="/aduan")

_FORM_FIELDS = [
    "tanggal_aduan", "id_simpang", "lokasi_simpang", "detail_posisi",
    "jenis_gangguan", "penyebab_gangguan", "pelapor",
]


def _read_form():
    return {field: request.form.get(field, "").strip() for field in _FORM_FIELDS}


@bp.route("")
def index():
    return render_template("aduan/index.html", aduan=aduan_model.get_all())


@bp.route("/detail/<int:id_aduan>")
def detail(id_aduan):
    data = aduan_model.get_detail(id_aduan)
    if data is None:
        return "Data aduan tidak ditemukan", 404
    return render_template("aduan/detail.html", data=data)


@bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        data = _read_form()

        try:
            foto = save_uploaded_photo(
                request.files.get("foto_kondisi_awal")
            )
        except ValueError as e:
            return str(e), 400

        try:
            id_aduan = aduan_model.create(data, foto)
        except Exception as e:
            return f"Terjadi error: {e}", 500

        return redirect(url_for("aduan.detail", id_aduan=id_aduan))

    return render_template(
        "aduan/form.html",
        simpang=simpang_model.get_dropdown_list(),
        edit=False,
        data=None,
    )


@bp.route("/edit/<int:id_aduan>", methods=["GET", "POST"])
def edit(id_aduan):
    if request.method == "POST":
        data = _read_form()

        try:
            foto_baru = save_uploaded_photo(
                request.files.get("foto_kondisi_awal")
            )
        except ValueError as e:
            return str(e), 400

        try:
            aduan_model.update(id_aduan, data, foto_baru)
        except Exception as e:
            return f"Terjadi error: {e}", 500

        return redirect(url_for("aduan.detail", id_aduan=id_aduan))

    data = aduan_model.get_for_edit(id_aduan)
    if data is None:
        return "Data aduan tidak ditemukan", 404

    return render_template(
        "aduan/form.html",
        data=data,
        simpang=simpang_model.get_dropdown_list(),
        edit=True,
    )


@bp.route("/<int:id_aduan>/penanganan", methods=["POST"])
def penanganan(id_aduan):
    tindak_lanjut = request.form.get("tindak_lanjut", "").strip()
    pic = request.form.get("pic", "").strip()
    waktu_tl = request.form.get("waktu_tl", "").strip()

    try:
        foto_proses_tl = save_uploaded_photo(
            request.files.get("foto_proses_tl"), prefix="proses_"
        )
        foto_kondisi_akhir = save_uploaded_photo(
            request.files.get("foto_kondisi_akhir"), prefix="akhir_"
        )
    except ValueError as e:
        return str(e), 400

    try:
        aduan_model.update_penanganan(
            id_aduan, tindak_lanjut, pic, waktu_tl,
            foto_proses_tl, foto_kondisi_akhir,
        )
    except Exception as e:
        return f"Error penanganan: {e}", 500

    return redirect(url_for("aduan.detail", id_aduan=id_aduan))


@bp.route("/hapus/<int:id_aduan>", methods=["POST"])
def hapus(id_aduan):
    try:
        aduan_model.delete(id_aduan)
    except Exception as e:
        return f"Error hapus aduan: {e}", 500
    return redirect(url_for("aduan.index"))
