from dataclasses import dataclass, field
from enum import IntEnum
from car import CarSpecs, PlatformConfig, Platforms
from car.docs_definitions import CarInfo, CarParts

class CarControllerParams:
    # Limites de torque para a direção elétrica (EPS)
    # Estes valores são conservadores para começar com segurança
    STEER_MAX = 300           # Torque máximo permitido
    STEER_DELTA_UP = 3        # Incremento máximo de torque por frame
    STEER_DELTA_DOWN = 7      # Decremento máximo de torque por frame
    STEER_DRIVER_ALLOWANCE = 50 # Quanto torque o condutor pode aplicar antes de o OP ceder
    STEER_DRIVER_MULTIPLIER = 2 # Sensibilidade da resistência do condutor
    STEER_DRIVER_FACTOR = 1    # Factor de escala

@dataclass
class RenaultCarInfo(CarInfo):
    package: str = "Pack Advanced Driving Assist"
    maintainer: str = "jailsonmachado" # O seu nome como desenvolvedor do port

class CAR(Platforms):
    # Definição da plataforma Megane E-Tech
    MEGANE_ETECH = PlatformConfig(
        "RENAULT MEGANE E-TECH",
        RenaultCarInfo("Renault Megane E-Tech 2022+"),
        CarSpecs(
            mass=1708.0,       # Peso aproximado em kg (ajustar conforme a sua versão)
            wheelbase=2.68,    # Distância entre eixos em metros
            steerRatio=14.5,   # Relação de direção (estimada, comum em Renaults novos)
            centerToFront=None # Será calculado automaticamente se deixado como None
        )
    )

# IDs das mensagens CAN que identificamos no seu log
class CAN:
    ADAS_STATUS = 0x1ab   # A mensagem de 48 bytes com Checksum e Counter
    WHEEL_SPEEDS = 0x226  # Velocidade das rodas
    GAS_PEDAL = 0x12f     # Posição do acelerador
