from dataclasses import dataclass
from enum import IntEnum
from car.docs_definitions import CarFootnote, CarInfo, CarParts
from car import CarSpecs, PlatformConfig, Platforms

class CarControllerParams:
    STEER_MAX = 300       # Valor máximo de torque (ajustar depois)
    STEER_DELTA_UP = 3    # Quão rápido o volante pode subir o torque
    STEER_DELTA_DOWN = 7  # Quão rápido o torque pode cair
    STEER_DRIVER_ALLOWANCE = 50 

class CAN:
    # IDs que confirmamos no seu log
    ADAS_STATUS = 0x1ab   # 100Hz
    WHEEL_SPEEDS = 0x226  # 50Hz
    GAS_PEDAL = 0x12f     # 100Hz

@dataclass
class RenaultCarInfo(CarInfo):
    package: str = "Todos os modelos"

class CAR(Platforms):
    MEGANE_ETECH = PlatformConfig(
        "RENAULT MEGANE E-TECH",
        RenaultCarInfo("Renault Megane E-Tech 2022+"),
        CarSpecs(mass=1708., wheelbase=2.68, steerRatio=14.5)
    )
