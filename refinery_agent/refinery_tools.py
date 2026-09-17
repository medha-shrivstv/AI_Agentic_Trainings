# refinery_tools.py

import random
from datetime import datetime

# Simulated refinery units
REFINERY_UNITS = {
    "CDU-1": {
        "name": "Crude Distillation Unit 1",
        "type": "distillation",
    },
    "FCC-2": {
        "name": "Fluid Catalytic Cracker 2",
        "type": "cracking",
    },
    "HDS-3": {
        "name": "Hydrodesulfurization Unit 3",
        "type": "treatment",
    },
}


def get_sensor_reading(
    equipment_id: str,
    sensor_type: str,
) -> dict:
    """
    Simulate a live sensor reading.
    """

    baseline = {
        "temperature_C": 370,
        "pressure_bar": 12,
        "flow_rate_m3h": 850,
    }

    value = baseline.get(sensor_type, 0)

    # Simulated anomaly
    if (
        equipment_id == "FCC-2"
        and sensor_type == "temperature_C"
    ):
        value = 512

    noise = random.uniform(-2, 2)

    return {
        "equipment_id": equipment_id,
        "sensor_type": sensor_type,
        "value": round(value + noise, 1),
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
    }


def get_equipment_status(
    equipment_id: str,
) -> dict:
    """
    Simulate control-room status.
    """

    status = (
        "running_degraded"
        if equipment_id == "FCC-2"
        else "running"
    )

    return {
        "equipment_id": equipment_id,
        "status": status,
    }


def check_maintenance_schedule(
    equipment_id: str,
) -> dict:
    """
    Simulate maintenance system lookup.
    """

    last_service = {
        "CDU-1": "2026-04-02",
        "FCC-2": "2025-11-18",
        "HDS-3": "2026-05-30",
    }

    return {
        "equipment_id": equipment_id,
        "last_service_date": last_service.get(
            equipment_id,
            "unknown",
        ),
        "service_interval": "every 6 months",
    }


def get_historical_trend(
    equipment_id: str,
    sensor_type: str,
    hours: int,
) -> dict:
    """
    Simulate historical sensor data.
    """

    base = (
        500
        if equipment_id == "FCC-2"
        else 370
    )

    trend = []

    for h in range(hours, 0, -1):

        drift = (
            (hours - h) * 1.5
            if equipment_id == "FCC-2"
            else 0
        )

        trend.append(
            round(
                base
                + drift
                + random.uniform(-1, 1),
                1,
            )
        )

    return {
        "equipment_id": equipment_id,
        "sensor_type": sensor_type,
        "trend_last_n_hours": trend,
    }


def trigger_safety_alert(
    equipment_id: str,
    message: str,
) -> dict:
    """
    Simulate raising a safety alert.
    """

    return {
        "equipment_id": equipment_id,
        "alert_raised": True,
        "message": message,
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
    }


if __name__ == "__main__":

    print("\nSensor Test")
    print(
        get_sensor_reading(
            "FCC-2",
            "temperature_C",
        )
    )

    print("\nStatus Test")
    print(
        get_equipment_status(
            "FCC-2"
        )
    )

    print("\nMaintenance Test")
    print(
        check_maintenance_schedule(
            "FCC-2"
        )
    )

    print("\nTrend Test")
    print(
        get_historical_trend(
            "FCC-2",
            "temperature_C",
            5,
        )
    )

    print("\nAlert Test")
    print(
        trigger_safety_alert(
            "FCC-2",
            "Temperature exceeds safe limit",
        )
    )