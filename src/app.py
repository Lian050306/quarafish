"""Web app Streamlit untuk QUARAFISH"""

import streamlit as st
import cv2
import time
import pandas as pd
from datetime import datetime

from config import (
    APP_NAME, APP_DESCRIPTION, APP_THEME, APP_FOOTER,
    REKOMENDASI,
    STATUS_NORMAL, STATUS_WASPADA, STATUS_BAHAYA
)
from sensor import baca_semua_sensor
from vision import deteksi_lingkungan, buka_kamera, ambil_frame, proses_frame
from utils import simpan_log


st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== CSS KUSTOM ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }
    .header-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
        padding: 32px 36px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(30, 58, 138, 0.35);
    }
    .header-title {
        font-size: 40px;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0;
    }
    .header-tagline {
        font-size: 18px;
        opacity: 0.98;
        margin-top: 10px;
        font-weight: 500;
    }
    .header-subtitle {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 12px;
        line-height: 1.6;
    }
    .theme-box {
        background: #fef3c7;
        padding: 14px 22px;
        border-radius: 10px;
        border-left: 5px solid #d97706;
        color: #78350f;
        font-style: italic;
        margin-bottom: 22px;
        font-size: 15px;
    }

    /* Section title */
    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #1e3a8a;
        margin-top: 10px;
        margin-bottom: 18px;
        border-left: 6px solid #1d4ed8;
        padding-left: 14px;
    }

    /* Kartu umum */
    .card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        height: 100%;
    }
    .card-title {
        font-size: 18px;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 12px;
    }
    .card-text {
        font-size: 15px;
        line-height: 1.7;
        color: #334155;
    }

    /* Kartu ikan sehat */
    .card-sehat {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 6px solid #16a34a;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 2px 12px rgba(22, 163, 74, 0.15);
        margin-bottom: 16px;
        height: 100%;
    }
    .card-sehat .card-title {
        color: #166534;
        font-size: 20px;
    }
    .card-sehat ul {
        margin: 8px 0 0 0;
        padding-left: 20px;
        color: #14532d;
        line-height: 1.9;
        font-size: 15px;
    }

    /* Kartu ikan tidak sehat */
    .card-tidak-sehat {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 6px solid #dc2626;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 2px 12px rgba(220, 38, 38, 0.15);
        margin-bottom: 16px;
        height: 100%;
    }
    .card-tidak-sehat .card-title {
        color: #991b1b;
        font-size: 20px;
    }
    .card-tidak-sehat ul {
        margin: 8px 0 0 0;
        padding-left: 20px;
        color: #7f1d1d;
        line-height: 1.9;
        font-size: 15px;
    }

    /* Statistik ringkas */
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-top: 4px solid #1d4ed8;
    }
    .stat-value {
        font-size: 32px;
        font-weight: 800;
        color: #1e3a8a;
    }
    .stat-label {
        font-size: 13px;
        color: #64748b;
        margin-top: 6px;
        font-weight: 600;
    }

    /* Langkah dashboard */
    .langkah-box {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-top: 4px solid #1d4ed8;
        height: 100%;
        text-align: center;
    }
    .langkah-nomor {
        background: #1d4ed8;
        color: white;
        font-size: 22px;
        font-weight: 800;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }
    .langkah-judul {
        font-weight: 800;
        color: #1e3a8a;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .langkah-teks {
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
    }

    /* Kartu metrik dashboard */
    .metric-box {
        background: white;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-top: 4px solid #1d4ed8;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #1e3a8a;
    }
    .metric-label {
        font-size: 13px;
        color: #64748b;
        margin-top: 6px;
        font-weight: 600;
    }

    /* Status kotak */
    .status-normal {
        background: #dcfce7;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #16a34a;
        color: #166534;
        font-weight: 700;
        font-size: 18px;
    }
    .status-waspada {
        background: #fef9c3;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #ca8a04;
        color: #854d0e;
        font-weight: 700;
        font-size: 18px;
    }
    .status-bahaya {
        background: #fee2e2;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #dc2626;
        color: #991b1b;
        font-weight: 700;
        font-size: 18px;
    }

    /* Sensor */
    .sensor-card {
        background: white;
        padding: 14px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 10px;
        border-left: 4px solid #0284c7;
    }
    .sensor-label {
        font-size: 12px;
        color: #64748b;
        font-weight: 600;
    }
    .sensor-value {
        font-size: 22px;
        color: #0f172a;
        font-weight: 800;
    }

    .info-cloud {
        background: #dbeafe;
        padding: 14px 18px;
        border-radius: 10px;
        border-left: 5px solid #1d4ed8;
        color: #1e3a8a;
        margin-bottom: 18px;
        font-size: 14px;
    }

    /* Tombol navigasi halaman */
    .stButton > button[kind="primary"] {
        background: #1d4ed8;
        color: white;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ==================== STATE ====================
if "halaman" not in st.session_state:
    st.session_state.halaman = "pengenalan"

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "total_baca" not in st.session_state:
    st.session_state.total_baca = 0
if "total_normal" not in st.session_state:
    st.session_state.total_normal = 0
if "total_waspada" not in st.session_state:
    st.session_state.total_waspada = 0
if "total_bahaya" not in st.session_state:
    st.session_state.total_bahaya = 0
if "sensor_terakhir" not in st.session_state:
    st.session_state.sensor_terakhir = {
        "uv": 0, "ph": 0, "suhu": 0, "status": STATUS_NORMAL
    }


# ==================== FUNGSI ====================
def mainkan_alarm():
    html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(html, unsafe_allow_html=True)


def catat_riwayat(data):
    waktu = datetime.now().strftime("%H:%M:%S")
    st.session_state.riwayat.insert(0, {
        "Waktu": waktu,
        "UV": data["uv"],
        "pH": data["ph"],
        "Suhu": data["suhu"],
        "Status": data["status"],
        "Tindakan": REKOMENDASI[data["status"]]
    })
    if len(st.session_state.riwayat) > 50:
        st.session_state.riwayat = st.session_state.riwayat[:50]

    st.session_state.total_baca += 1
    if data["status"] == STATUS_NORMAL:
        st.session_state.total_normal += 1
    elif data["status"] == STATUS_WASPADA:
        st.session_state.total_waspada += 1
    else:
        st.session_state.total_bahaya += 1


def render_status(data):
    status = data["status"]
    if status == STATUS_NORMAL:
        st.markdown(f"""
        <div class="status-normal">
            STATUS: {status}<br>
            <small>{REKOMENDASI[status]}</small>
        </div>
        """, unsafe_allow_html=True)
    elif status == STATUS_WASPADA:
        st.markdown(f"""
        <div class="status-waspada">
            STATUS: {status}<br>
            <small>{REKOMENDASI[status]}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-bahaya">
            STATUS: {status}<br>
            <small>{REKOMENDASI[status]}</small>
        </div>
        """, unsafe_allow_html=True)


def render_sensor(data):
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
        <div class="sensor-card">
            <div class="sensor-label">SENSOR UV</div>
            <div class="sensor-value">{data['uv']}</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="sensor-card">
            <div class="sensor-label">pH AIR</div>
            <div class="sensor-value">{data['ph']}</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="sensor-card">
            <div class="sensor-label">SUHU (C)</div>
            <div class="sensor-value">{data['suhu']}</div>
        </div>
        """, unsafe_allow_html=True)


# ==================== HALAMAN PENGENALAN ====================
def halaman_pengenalan():
    st.markdown(f"""
    <div class="header-box">
        <div class="header-title">QUARAFISH</div>
        <div class="header-tagline">Sistem Peringatan Dini Kesehatan Ikan Berbasis UV-IoT</div>
        <div class="header-subtitle">
            Deteksi lebih dini, tindakan lebih cepat, risiko lebih terkendali,
            dan ikan yang lebih aman untuk ekspor Indonesia.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="theme-box">
        Tema QIC 2026: {APP_THEME}
    </div>
    """, unsafe_allow_html=True)

    # ====== Tentang QUARAFISH ======
    st.markdown('<div class="section-title">Tentang QUARAFISH</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-text">
            <b>QUARAFISH</b> hadir sebagai langkah awal dalam menjaga kesehatan
            dan keamanan komoditas perikanan. Melalui pemeriksaan berbasis
            <b>sinar UV</b> yang terintegrasi dengan <b>sistem digital</b>,
            QUARAFISH membantu mengenali indikasi awal kelainan atau penyakit
            pada ikan, mencatat hasil pemeriksaan, dan memberikan peringatan
            risiko secara cepat.
            <br><br>
            Sistem ini dirancang untuk mendukung <b>petugas karantina</b>
            dalam melakukan pemantauan, mitigasi, dan penguatan biosekuriti
            perikanan karena deteksi lebih dini berarti tindakan lebih cepat,
            risiko lebih terkendali, dan ikan yang lebih aman.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ====== Ciri Ikan Sehat dan Tidak Sehat ======
    st.markdown('<div class="section-title">Ciri-Ciri Ikan</div>', unsafe_allow_html=True)

    col_sehat, col_tidak = st.columns(2)

    with col_sehat:
        st.markdown("""
        <div class="card-sehat">
            <div class="card-title">IKAN SEHAT</div>
            <ul>
                <li>Mata jernih, cerah, dan menonjol</li>
                <li>Sisik rapi, mengkilap, dan melekat kuat</li>
                <li>Insang berwarna merah segar</li>
                <li>Gerakan aktif dan responsif</li>
                <li>Tubuh tidak ada luka atau benjolan</li>
                <li>Warna tubuh cerah dan merata</li>
                <li>Nafsu makan normal</li>
                <li>Berenang tegak dan stabil</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_tidak:
        st.markdown("""
        <div class="card-tidak-sehat">
            <div class="card-title">IKAN TIDAK SEHAT</div>
            <ul>
                <li>Mata keruh, pucat, atau berdarah</li>
                <li>Sisik lepas, kusam, atau berjamur</li>
                <li>Insang pucat, coklat, atau berlendir</li>
                <li>Gerakan lemas dan tidak responsif</li>
                <li>Ada luka, borok, atau benjolan</li>
                <li>Warna tubuh pucat dan tidak merata</li>
                <li>Nafsu makan menurun</li>
                <li>Berenang miring atau tidak stabil</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ====== Dashboard Pengenalan ======
    st.markdown('<div class="section-title">Cara Menggunakan Dashboard</div>', unsafe_allow_html=True)

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        st.markdown("""
        <div class="langkah-box">
            <div class="langkah-nomor">1</div>
            <div class="langkah-judul">Buka Dashboard</div>
            <div class="langkah-teks">
                Klik menu <b>Dashboard</b> di sidebar untuk masuk ke halaman pemantauan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with l2:
        st.markdown("""
        <div class="langkah-box">
            <div class="langkah-nomor">2</div>
            <div class="langkah-judul">Masukkan Ikan</div>
            <div class="langkah-teks">
                Letakkan box ikan di depan kamera. Sistem akan memindai ikan secara otomatis.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with l3:
        st.markdown("""
        <div class="langkah-box">
            <div class="langkah-nomor">3</div>
            <div class="langkah-judul">Lihat Hasil</div>
            <div class="langkah-teks">
                Hasil pemindaian ditampilkan di layar:
                <b>titik hijau</b> untuk ikan sehat, <b>titik merah</b> untuk ikan tidak sehat.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with l4:
        st.markdown("""
        <div class="langkah-box">
            <div class="langkah-nomor">4</div>
            <div class="langkah-judul">Tindak Lanjut</div>
            <div class="langkah-teks">
                Jika ikan tidak sehat, alarm berbunyi dan box ditolak untuk pemeriksaan lanjutan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ====== Statistik Sistem ======
    st.markdown('<div class="section-title">Statistik Sistem</div>', unsafe_allow_html=True)

    sm1, sm2, sm3, sm4 = st.columns(4)

    with sm1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{st.session_state.total_baca}</div>
            <div class="stat-label">Total Pemindaian</div>
        </div>
        """, unsafe_allow_html=True)

    with sm2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value" style="color:#16a34a;">{st.session_state.total_normal}</div>
            <div class="stat-label">Ikan Sehat</div>
        </div>
        """, unsafe_allow_html=True)

    with sm3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value" style="color:#ca8a04;">{st.session_state.total_waspada}</div>
            <div class="stat-label">Perlu Dicek</div>
        </div>
        """, unsafe_allow_html=True)

    with sm4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value" style="color:#dc2626;">{st.session_state.total_bahaya}</div>
            <div class="stat-label">Ikan Tidak Sehat</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ====== Tombol ke Dashboard ======
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("Buka Dashboard Pemantauan", type="primary", width='stretch'):
            st.session_state.halaman = "dashboard"
            st.rerun()


# ==================== HALAMAN DASHBOARD ====================
def halaman_dashboard():
    lingkungan = deteksi_lingkungan()

    st.markdown(f"""
    <div class="header-box">
        <div class="header-title">QUARAFISH</div>
        <div class="header-subtitle">{APP_DESCRIPTION}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="theme-box">
        Tema QIC 2026: {APP_THEME}
    </div>
    """, unsafe_allow_html=True)

    if lingkungan == "cloud":
        st.markdown("""
        <div class="info-cloud">
            <b>Catatan:</b> Anda mengakses versi cloud. Kamera live hanya tersedia
            di versi lokal. Untuk versi cloud, sistem menampilkan pemantauan sensor
            UV-IoT dan simulasi deteksi.
        </div>
        """, unsafe_allow_html=True)

    # ====== Metrik ======
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{st.session_state.total_baca}</div>
            <div class="metric-label">Total Deteksi</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color:#16a34a;">{st.session_state.total_normal}</div>
            <div class="metric-label">Normal</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color:#ca8a04;">{st.session_state.total_waspada}</div>
            <div class="metric-label">Waspada</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color:#dc2626;">{st.session_state.total_bahaya}</div>
            <div class="metric-label">Bahaya</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ====== Layout utama ======
    col1, col2 = st.columns([2, 1])

    with col1:
        if lingkungan == "lokal":
            st.markdown("### Kamera & Deteksi Visual")
        else:
            st.markdown("### Simulasi Deteksi Visual (Cloud)")
        frame_placeholder = st.empty()

    with col2:
        st.markdown("### Panel Sensor UV-IoT")
        sensor_placeholder = st.empty()
        st.markdown("### Status Peringatan Dini")
        status_placeholder = st.empty()
        alarm_placeholder = st.empty()

    # ====== Kontrol ======
    st.markdown("---")
    st.markdown("### Kontrol Pemantauan")

    if lingkungan == "lokal":
        tombol_col1, tombol_col2, tombol_col3 = st.columns(3)

        with tombol_col1:
            if st.button("Mulai Pemantauan", type="primary", width='stretch'):
                st.session_state.monitoring = True

        with tombol_col2:
            if st.button("Hentikan Pemantauan", width='stretch'):
                st.session_state.monitoring = False

        with tombol_col3:
            if st.button("Deteksi Sekali", width='stretch'):
                data = baca_semua_sensor()
                st.session_state.sensor_terakhir = data
                catat_riwayat(data)

                cap = buka_kamera()
                if cap is not None:
                    frame = ambil_frame(cap)
                    if frame is not None:
                        frame = proses_frame(frame, data["status"])
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(frame_rgb, channels="RGB", width='stretch')
                    cap.release()

                if data["status"] == STATUS_BAHAYA:
                    simpan_log(f"BAHAYA: UV={data['uv']} pH={data['ph']} Suhu={data['suhu']}")
                    mainkan_alarm()

                st.rerun()
    else:
        tombol_col1, tombol_col2 = st.columns(2)

        with tombol_col1:
            if st.button("Mulai Pemantauan Sensor", type="primary", width='stretch'):
                st.session_state.monitoring = True

        with tombol_col2:
            if st.button("Hentikan Pemantauan", width='stretch'):
                st.session_state.monitoring = False

    # ====== Loop Pemantauan ======
    if st.session_state.monitoring:
        if lingkungan == "lokal":
            cap = buka_kamera()
            if cap is None:
                st.error("Kamera tidak terdeteksi. Coba cek koneksi kamera.")
                st.session_state.monitoring = False
            else:
                while st.session_state.monitoring:
                    data = baca_semua_sensor()
                    st.session_state.sensor_terakhir = data
                    catat_riwayat(data)

                    frame = ambil_frame(cap)
                    if frame is not None:
                        frame = proses_frame(frame, data["status"])
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(frame_rgb, channels="RGB", width='stretch')

                    with sensor_placeholder.container():
                        render_sensor(data)
                    with status_placeholder.container():
                        render_status(data)

                    if data["status"] == STATUS_BAHAYA:
                        alarm_placeholder.error("ALARM: Parameter tidak normal - risiko penyakit ikan")
                        simpan_log(f"BAHAYA: UV={data['uv']} pH={data['ph']} Suhu={data['suhu']}")
                        mainkan_alarm()
                    elif data["status"] == STATUS_WASPADA:
                        alarm_placeholder.warning("Peringatan: Parameter mendekati batas tidak normal")
                    else:
                        alarm_placeholder.info("Kondisi normal - tidak ada peringatan")

                    time.sleep(interval)
                cap.release()
        else:
            while st.session_state.monitoring:
                data = baca_semua_sensor()
                st.session_state.sensor_terakhir = data
                catat_riwayat(data)

                with sensor_placeholder.container():
                    render_sensor(data)
                with status_placeholder.container():
                    render_status(data)

                if data["status"] == STATUS_BAHAYA:
                    alarm_placeholder.error("ALARM: Parameter tidak normal - risiko penyakit ikan")
                    simpan_log(f"BAHAYA: UV={data['uv']} pH={data['ph']} Suhu={data['suhu']}")
                    mainkan_alarm()
                elif data["status"] == STATUS_WASPADA:
                    alarm_placeholder.warning("Peringatan: Parameter mendekati batas tidak normal")
                else:
                    alarm_placeholder.info("Kondisi normal - tidak ada peringatan")

                time.sleep(interval)

    else:
        data = st.session_state.sensor_terakhir
        if st.session_state.total_baca > 0:
            with sensor_placeholder.container():
                render_sensor(data)
            with status_placeholder.container():
                render_status(data)
            alarm_placeholder.info("Pemantauan tidak aktif")
        else:
            if lingkungan == "lokal":
                frame_placeholder.info("Pemantauan tidak aktif. Klik Mulai Pemantauan.")
            else:
                frame_placeholder.info("Pemantauan tidak aktif. Klik Mulai Pemantauan Sensor.")

    # ====== Riwayat & Grafik ======
    st.markdown("---")
    col_r1, col_r2 = st.columns([2, 1])

    with col_r1:
        st.markdown("### Riwayat Deteksi")
        if st.session_state.riwayat:
            df = pd.DataFrame(st.session_state.riwayat)
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.info("Belum ada riwayat deteksi.")

    with col_r2:
        st.markdown("### Distribusi Status")
        if st.session_state.total_baca > 0:
            chart_data = pd.DataFrame({
                "Status": ["Normal", "Waspada", "Bahaya"],
                "Jumlah": [
                    st.session_state.total_normal,
                    st.session_state.total_waspada,
                    st.session_state.total_bahaya
                ]
            })
            st.bar_chart(chart_data, x="Status", y="Jumlah")
        else:
            st.info("Belum ada data.")

    # ====== Info bawah ======
    st.markdown("---")
    col_i1, col_i2, col_i3 = st.columns(3)

    with col_i1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Tujuan</div>
            <div class="card-text">
                Peringatan dini dan mitigasi risiko penyakit ikan di pos karantina
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_i2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Teknologi</div>
            <div class="card-text">
                Kamera, sensor UV-IoT, dan dashboard web terintegrasi
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_i3:
        st.markdown("""
        <div class="card">
            <div class="card-title">Ajang</div>
            <div class="card-text">
                QIC 2026 - Badan Karantina Indonesia
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### Navigasi")

    if st.button("Halaman Pengenalan", width='stretch',
                 type="primary" if st.session_state.halaman == "pengenalan" else "secondary"):
        st.session_state.halaman = "pengenalan"
        st.rerun()

    if st.button("Dashboard Pemantauan", width='stretch',
                 type="primary" if st.session_state.halaman == "dashboard" else "secondary"):
        st.session_state.halaman = "dashboard"
        st.rerun()

    st.divider()

    st.markdown("### Pengaturan Sistem")
    interval = st.slider("Interval deteksi (detik)", 1, 5, 2)

    st.divider()
    st.markdown("### Status Perangkat")
    lingkungan = deteksi_lingkungan()
    if lingkungan == "lokal":
        st.success("Kamera: Aktif")
    else:
        st.warning("Kamera: Tidak tersedia (cloud)")
    st.success("Sensor UV: Terhubung")
    st.success("Sensor pH: Terhubung")
    st.success("Sensor Suhu: Terhubung")
    st.info("Koneksi IoT: Aktif")

    st.divider()
    st.markdown("### Tentang")
    st.markdown("""
    **QUARAFISH** — Sistem peringatan dini kesehatan ikan
    berbasis UV-IoT untuk biosekuriti karantina perikanan.
    """)

    st.divider()
    if st.button("Reset Statistik", width='stretch'):
        st.session_state.riwayat = []
        st.session_state.total_baca = 0
        st.session_state.total_normal = 0
        st.session_state.total_waspada = 0
        st.session_state.total_bahaya = 0
        st.rerun()


# ==================== ROUTING HALAMAN ====================
if st.session_state.halaman == "pengenalan":
    halaman_pengenalan()
else:
    halaman_dashboard()

st.markdown("---")
st.caption(APP_FOOTER)