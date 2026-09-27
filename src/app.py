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
from vision import buka_kamera, ambil_frame, proses_frame
from utils import simpan_log


st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }
    .header-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
        padding: 28px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.35);
    }
    .header-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0;
    }
    .header-subtitle {
        font-size: 16px;
        opacity: 0.95;
        margin-top: 8px;
        line-height: 1.5;
    }
    .theme-box {
        background: #fef3c7;
        padding: 12px 20px;
        border-radius: 10px;
        border-left: 5px solid #d97706;
        color: #78350f;
        font-style: italic;
        margin-bottom: 18px;
    }
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
    .info-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 5px solid #1d4ed8;
        height: 100%;
    }
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
</style>
""", unsafe_allow_html=True)


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


def mainkan_alarm():
    """Bunyi alarm saat status BAHAYA"""
    html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg">
    </audio>
    """
    st.components.v1.html(html, height=0)


def catat_riwayat(data):
    """Catat hasil pembacaan ke riwayat"""
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
    """Tampilkan kotak status"""
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
    """Tampilkan 3 kartu sensor"""
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


with st.sidebar:
    st.markdown("### Pengaturan Sistem")
    interval = st.slider("Interval deteksi (detik)", 1, 5, 2)

    st.divider()
    st.markdown("### Status Perangkat")
    st.success("Kamera: Aktif")
    st.success("Sensor UV: Terhubung")
    st.success("Sensor pH: Terhubung")
    st.success("Sensor Suhu: Terhubung")
    st.info("Koneksi IoT: Aktif")

    st.divider()
    st.markdown("### Tentang QUARAFISH")
    st.markdown("""
    **QUARAFISH** adalah sistem peringatan dini dan mitigasi risiko
    penyakit ikan berbasis UV-IoT dan kamera (computer vision),
    terintegrasi dengan dashboard web untuk mendukung biosekuriti
    di pos karantina perikanan.
    """)

    st.divider()
    if st.button("Reset Statistik", use_container_width=True):
        st.session_state.riwayat = []
        st.session_state.total_baca = 0
        st.session_state.total_normal = 0
        st.session_state.total_waspada = 0
        st.session_state.total_bahaya = 0
        st.rerun()


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


col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Kamera & Deteksi Visual")
    frame_placeholder = st.empty()

with col2:
    st.markdown("### Panel Sensor UV-IoT")
    sensor_placeholder = st.empty()
    st.markdown("### Status Peringatan Dini")
    status_placeholder = st.empty()
    alarm_placeholder = st.empty()


st.markdown("---")
st.markdown("### Kontrol Pemantauan")

tombol_col1, tombol_col2, tombol_col3 = st.columns(3)

with tombol_col1:
    if st.button("Mulai Pemantauan", type="primary", use_container_width=True):
        st.session_state.monitoring = True

with tombol_col2:
    if st.button("Hentikan Pemantauan", use_container_width=True):
        st.session_state.monitoring = False

with tombol_col3:
    if st.button("Deteksi Sekali", use_container_width=True):
        data = baca_semua_sensor()
        st.session_state.sensor_terakhir = data
        catat_riwayat(data)

        cap = buka_kamera()
        if cap is not None:
            frame = ambil_frame(cap)
            if frame is not None:
                frame = proses_frame(frame, data["status"])
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            cap.release()

        if data["status"] == STATUS_BAHAYA:
            simpan_log(f"BAHAYA: UV={data['uv']} pH={data['ph']} Suhu={data['suhu']}")
            mainkan_alarm()

        st.rerun()


if st.session_state.monitoring:
    cap = buka_kamera()

    if cap is None:
        st.error("Kamera tidak terdeteksi. Cek koneksi kamera.")
        st.session_state.monitoring = False
    else:
        while st.session_state.monitoring:
            data = baca_semua_sensor()
            st.session_state.sensor_terakhir = data
            catat_riwayat(data)

            # Ambil frame kamera + proses
            frame = ambil_frame(cap)
            if frame is not None:
                frame = proses_frame(frame, data["status"])
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            # Panel sensor
            with sensor_placeholder.container():
                render_sensor(data)

            # Status
            with status_placeholder.container():
                render_status(data)

            # Alarm
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
    data = st.session_state.sensor_terakhir
    if st.session_state.total_baca > 0:
        with sensor_placeholder.container():
            render_sensor(data)
        with status_placeholder.container():
            render_status(data)
        alarm_placeholder.info("Pemantauan tidak aktif")
    else:
        frame_placeholder.info("Pemantauan tidak aktif. Klik Mulai Pemantauan atau Deteksi Sekali.")


st.markdown("---")
col_r1, col_r2 = st.columns([2, 1])

with col_r1:
    st.markdown("### Riwayat Deteksi")
    if st.session_state.riwayat:
        df = pd.DataFrame(st.session_state.riwayat)
        st.dataframe(df, use_container_width=True, hide_index=True)
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


st.markdown("---")
col_i1, col_i2, col_i3 = st.columns(3)

with col_i1:
    st.markdown("""
    <div class="info-card">
        <b>Tujuan</b><br>
        Peringatan dini dan mitigasi risiko penyakit ikan di pos karantina
    </div>
    """, unsafe_allow_html=True)

with col_i2:
    st.markdown("""
    <div class="info-card">
        <b>Teknologi</b><br>
        Kamera, sensor UV-IoT, dan dashboard web terintegrasi
    </div>
    """, unsafe_allow_html=True)

with col_i3:
    st.markdown("""
    <div class="info-card">
        <b>Ajang</b><br>
        QIC 2026 - Badan Karantina Indonesia
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")
st.caption(APP_FOOTER)