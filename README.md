# QUARAFISH

Sistem Peringatan Dini dan Mitigasi Risiko Penyakit Ikan Berbasis UV-IoT
Terintegrasi Web untuk Mendukung Biosekuriti Karantina Perikanan.

## Tema QIC 2026
Inovasi Generasi Muda Melindungi Hayati Nusantara dan Mengakselerasi
Ekspor Menuju Kedaulatan Ekonomi Global.

## Fitur
- Kamera deteksi box ikan (titik merah/hijau)
- Sensor UV, pH, suhu via IoT
- Peringatan dini (Normal / Waspada / Bahaya)
- Alarm otomatis saat BAHAYA
- Riwayat dan statistik

## Cara Menjalankan

1. Buat virtual environment:
   python -m venv venv

2. Aktifkan venv (Windows):
   .\venv\Scripts\Activate.ps1

3. Install library:
   pip install -r requirements.txt

4. Jalankan web:
   streamlit run src/app.py