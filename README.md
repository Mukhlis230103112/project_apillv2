# Sistem Inventaris APILL

## Struktur Project

```
project_apill/
├── app.py                  # Application factory, mendaftarkan semua blueprint
├── config.py                # Konfigurasi (DB, secret key, upload) dari .env
├── db.py                    # Koneksi database & context manager db_cursor()
├── utils.py                  # Helper validasi & penyimpanan foto upload
├── requirements.txt
├── blueprints/               # Routes, dikelompokkan per modul
│   ├── dashboard.py
│   ├── simpang.py
│   ├── perangkat.py
│   ├── monitoring.py
│   ├── aduan.py
│   ├── laporan.py
│   └── maps.py               # peta interaktif + endpoint GeoJSON
├── models/                   # Query SQL per entitas
│   ├── simpang.py
│   ├── perangkat.py
│   ├── monitoring.py
│   ├── aduan.py
│   ├── dashboard.py
│   └── laporan.py
├── templates/                 
└── static/
```

## Menjalankan

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```