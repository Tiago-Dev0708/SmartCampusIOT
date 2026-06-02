# Domain Entities
from .sensor_data import SensorDataEntity
from .classroom import ClassroomEntity
from .room import RoomEntity
from .external_sensors import ExternalSensorsEntity
from .dashboard import DashboardDataEntity, WeeklyDataPoint

__all__ = [
    "SensorDataEntity",
    "ClassroomEntity",
    "RoomEntity",
    "ExternalSensorsEntity",
    "DashboardDataEntity",
    "WeeklyDataPoint",
]
