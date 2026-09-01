import json

from flask import Blueprint, jsonify, render_template

from models import simpang as simpang_model

bp = Blueprint("maps", __name__)


@bp.route("/simpang/maps")
def index():
    return render_template("simpang/maps.html")


@bp.route("/api/simpang-geojson")
def simpang_geojson():
    rows = simpang_model.get_geojson_rows()
    data = [
        {
            "id_simpang": row[0],
            "kode_simpang": row[1],
            "nama_simpang": row[2],
            "jenis_simpang": row[3],
            "wilayah": row[4],
            "lat": float(row[5]),
            "lng": float(row[6]),
        }
        for row in rows
    ]
    return jsonify(data)


@bp.route("/api/batas-kabupaten")
def batas_kabupaten():
    with open("static/geo/batas_kabupaten.geojson", encoding="utf-8") as f:
        return jsonify(json.load(f))


@bp.route("/api/batas-kecamatan")
def batas_kecamatan():
    with open("static/geo/batas_kecamatan.geojson", encoding="utf-8") as f:
        return jsonify(json.load(f))
