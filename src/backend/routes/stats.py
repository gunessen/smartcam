import psutil
from flask import Blueprint, jsonify

from backend.schemas import StatsSchema

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/api/v1/stats", methods=["GET"])
def get_events():
    """
    Get system stats and return

    :return: current system stats
    """

    cpu_usage = psutil.cpu_percent(interval=1, percpu=False)

    # Calculate RAM stats
    ram_usage = psutil.virtual_memory()
    ram_total_mb = ram_usage.total / (1024 * 1024)
    ram_used_mb = ram_usage.used / (1024 * 1024)
    ram_used_percent = round(ram_usage.percent)

    # Calculate disk stats
    disk_usage = psutil.disk_usage("/")
    disk_total_gb = round(disk_usage.total / (1024 * 1024 * 1024), 1)
    disk_used_gb = round(disk_usage.used / (1024 * 1024 * 1024), 1)
    disk_used_percent = round(disk_usage.used / disk_usage.total * 100)

    stats = {
        "cpu_percent": cpu_usage,
        "ram_used_mb": ram_used_mb,
        "ram_total_mb": ram_total_mb,
        "ram_percent": ram_used_percent,
        "disk_used_gb": disk_used_gb,
        "disk_total_gb": disk_total_gb,
        "disk_percent": disk_used_percent,
    }

    return jsonify(StatsSchema().dump(stats))
