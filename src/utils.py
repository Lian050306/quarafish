"""Fungsi bantu untuk QUARAFISH"""

import cv2
import random
from datetime import datetime
from config import (
    UV_THRESHOLD_NORMAL, UV_THRESHOLD_WASPADA,
    PH_MIN, PH_MAX, SUHU_MIN, SUHU_MAX,
    STATUS_NORMAL, STATUS_WASPADA, STATUS_BAHAYA,
    COLOR_SEHAT, COLOR_TIDAK_SEHAT, COLOR_WASPADA,
    LABEL_SEHAT, LABEL_TIDAK_SEHAT,
    BOUNDING_BOX_MARGIN
)


def baca_sensor_uv():
    """Simulasi pembacaan sensor UV (IoT)"""
    return round(random.uniform(40, 100), 1)


def baca_sensor_ph():
    """Simulasi pembacaan sensor pH air"""
    return round(random.uniform(5.5, 9.0), 2)


def baca_sensor_suhu():
    """Simulasi pembacaan sensor suhu air"""
    return round(random.uniform(22, 32), 1)


def tentukan_status(uv, ph, suhu):
    """Tentukan status berdasarkan parameter sensor"""
    if (uv > UV_THRESHOLD_WASPADA or
            ph < PH_MIN or ph > PH_MAX or
            suhu < SUHU_MIN or suhu > SUHU_MAX):
        return STATUS_BAHAYA

    if uv > UV_THRESHOLD_NORMAL:
        return STATUS_WASPADA

    return STATUS_NORMAL


def gambar_bounding_box(frame, x1, y1, x2, y2, warna, label):
    """Gambar bounding box + label di frame"""
    cv2.rectangle(frame, (x1, y1), (x2, y2), warna, 3)
    cv2.putText(
        frame, label, (x1, y1 - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 1, warna, 3
    )
    return frame


def gambar_titik(frame, x, y, warna, radius=15):
    """Gambar titik di tengah bounding box"""
    cv2.circle(frame, (x, y), radius, warna, -1)
    return frame


def proses_deteksi_kamera(frame, status_sensor):
    """
    Gambar bounding box + titik pada frame kamera.
    Warna berdasarkan status sensor:
    - NORMAL  -> hijau (titik hijau)
    - WASPADA -> oranye
    - BAHAYA  -> merah (titik merah)
    """
    h, w = frame.shape[:2]

    x1 = int(w * BOUNDING_BOX_MARGIN)
    y1 = int(h * BOUNDING_BOX_MARGIN)
    x2 = int(w * (1 - BOUNDING_BOX_MARGIN))
    y2 = int(h * (1 - BOUNDING_BOX_MARGIN))

    if status_sensor == STATUS_NORMAL:
        warna = COLOR_SEHAT
        label = LABEL_SEHAT
    elif status_sensor == STATUS_WASPADA:
        warna = COLOR_WASPADA
        label = "WASPADA"
    else:
        warna = COLOR_TIDAK_SEHAT
        label = LABEL_TIDAK_SEHAT

    frame = gambar_bounding_box(frame, x1, y1, x2, y2, warna, label)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    frame = gambar_titik(frame, cx, cy, warna)

    return frame


def simpan_log(pesan):
    """Simpan log ke file"""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("logs/quarafish.log", "a") as f:
            f.write(f"[{waktu}] {pesan}\n")
    except FileNotFoundError:
        pass