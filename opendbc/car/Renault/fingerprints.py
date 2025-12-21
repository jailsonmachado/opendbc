from opendbc.car.structs import CarParams
from opendbc.car.renault.values import CAR

Ecu = CarParams.Ecu

# 1. Identificação por Versão de Firmware (Vazio por enquanto)
# Preencheremos quando você plugar o Comma no carro pela primeira vez.
FW_VERSIONS = {
    CAR.MEGANE_ETECH: {
        # Exemplo futuro: (Ecu.fwdCamera, 0x744, None): [b'12345ABC'],
    },
}

# 2. Identificação por Mensagens CAN (O que temos do seu log)
FINGERPRINTS = {
    CAR.MEGANE_ETECH: [
        {
            0x1ab: 48,  # ADAS_STATUS (CAN-FD 48 bytes)
            0x226: 48,  # WHEEL_SPEEDS (CAN-FD 48 bytes)
            0x12f: 12,  # GAS_PEDAL (CAN-FD 12 bytes)
            0x8c: 12,   # ID de alta frequência que vimos no log
            0xa8: 12,
            0x453: 12,
        },
    ]
}
