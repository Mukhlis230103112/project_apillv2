import os

from flask import Flask

from config import Config

from blueprints.aduan import bp as aduan_bp
from blueprints.dashboard import bp as dashboard_bp
from blueprints.laporan import bp as laporan_bp
from blueprints.maps import bp as maps_bp
from blueprints.monitoring import bp as monitoring_bp
from blueprints.perangkat import bp as perangkat_bp
from blueprints.simpang import bp as simpang_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(simpang_bp)
    app.register_blueprint(perangkat_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(aduan_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(maps_bp)

    return app


app = create_app()


# ==========================================
# JALANKAN FLASK
# ==========================================
if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
