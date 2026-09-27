"""Modul simulasi sensor UV-IoT"""

from utils import (
    baca_sensor_uv,
    baca_sensor_ph,
    baca_sensor_suhu,
    tentukan_status
)


def baca_semua_sensor():
    """Baca semua sensor (simulasi IoT)"""
    uv = baca_sensor_uv()
    ph = baca_sensor_ph()
    suhu = baca_sensor_suhu()

    status = tentukan_status(uv, ph, suhu)

    return {
        "uv": uv,
        "ph": ph,
        "suhu": suhu,
        "status": status
    }