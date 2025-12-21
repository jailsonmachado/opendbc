# opendbc/car/renault/fingerprints.py

from common.conversions import Conversions as CV
from opendbc.car.renault.values import CAR

# Estes são os IDs que o Comma 3X "vê" na rede CAN do seu Megane E-Tech.
# Se esses IDs baterem, ele carrega o seu port automaticamente.
FINGERPRINTS = {
  CAR.MEGANE_ETECH: {
    0x1ab: 48,  # ADAS_STATUS (CAN-FD 48 bytes)
    0x226: 48,  # WHEEL_SPEEDS (CAN-FD 48 bytes)
    0x12f: 12,  # GAS_PEDAL (CAN-FD 12 bytes)
    0x8c: 12,   # ID de alta frequência que vimos no log
    0xa8: 12,
    0x453: 12,
  }
}
