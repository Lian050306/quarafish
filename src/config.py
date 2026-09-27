"""Konfigurasi sistem QUARAFISH"""

# Identitas aplikasi
APP_NAME = "QUARAFISH"
APP_TITLE = "QUARAFISH - Sistem Peringatan Dini Penyakit Ikan"
APP_DESCRIPTION = (
    "Sistem Peringatan Dini dan Mitigasi Risiko Penyakit Ikan "
    "Berbasis UV-IoT Terintegrasi Web untuk Mendukung Biosekuriti "
    "Karantina Perikanan"
)
APP_THEME = (
    "Inovasi Generasi Muda Melindungi Hayati Nusantara dan "
    "Mengakselerasi Ekspor Menuju Kedaulatan Ekonomi Global"
)
APP_FOOTER = "QUARAFISH v0.1 | Prototipe Konsep QIC 2026 | Badan Karantina Indonesia"

# Kamera
CAMERA_ID = 0
BOUNDING_BOX_MARGIN = 0.3

# Warna BGR (OpenCV)
COLOR_SEHAT = (0, 200, 0)       # hijau
COLOR_TIDAK_SEHAT = (0, 0, 255) # merah
COLOR_WASPADA = (0, 165, 255)   # oranye

# Label
LABEL_SEHAT = "SEHAT"
LABEL_TIDAK_SEHAT = "TIDAK SEHAT"

# Batas parameter sensor UV (simulasi IoT)
UV_THRESHOLD_NORMAL = 70
UV_THRESHOLD_WASPADA = 85

PH_MIN = 6.5
PH_MAX = 8.5
SUHU_MIN = 25
SUHU_MAX = 30

# Status
STATUS_NORMAL = "NORMAL"
STATUS_WASPADA = "WASPADA"
STATUS_BAHAYA = "BAHAYA"

# Rekomendasi tindakan
REKOMENDASI = {
    "NORMAL": "Box ikan lolos karantina",
    "WASPADA": "Box ikan perlu pemeriksaan lanjutan",
    "BAHAYA": "Box ikan ditolak - risiko penyakit tinggi",
}