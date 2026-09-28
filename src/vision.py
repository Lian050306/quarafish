"""Modul kamera & deteksi visual"""

import cv2
from config import CAMERA_ID
from utils import proses_deteksi_kamera


def cek_kamera_tersedia():
    """
    Cek apakah kamera bisa dibuka.
    Return True kalau kamera ada & bisa diakses.
    """
    try:
        cap = cv2.VideoCapture(CAMERA_ID)
        if not cap.isOpened():
            return False
        ret, _ = cap.read()
        cap.release()
        return ret
    except Exception:
        return False


def deteksi_lingkungan():
    """
    Deteksi lingkungan:
    - Kalau kamera bisa dibuka -> 'lokal'
    - Kalau tidak -> 'cloud'
    """
    if cek_kamera_tersedia():
        return "lokal"
    return "cloud"


def buka_kamera():
    """Buka kamera dan kembalikan objek VideoCapture"""
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        return None
    return cap


def ambil_frame(cap):
    """Ambil 1 frame dari kamera"""
    ret, frame = cap.read()
    if not ret:
        return None
    return frame


def proses_frame(frame, status_sensor):
    """Proses frame: gambar bounding box + titik sesuai status sensor"""
    return proses_deteksi_kamera(frame, status_sensor)