from opendbc.can.parser import CANParser
from car.renault.values import CAN, CAR

class CarState:
    def __init__(self, CP):
        self.CP = CP
        self.cruise_buttons = 0
        self.is_metric = True

    def update(self, cp):
        ret = car.CarState.new_message()
        
        # Exemplo: Velocidade das Rodas (ID 0x226)
        # Os fatores (0.01) devem ser confirmados com o carro em movimento
        ret.wheelSpeeds.fl = cp.vl[CAN.WHEEL_SPEEDS]['WHEEL_SPEED_FL'] * 0.01
        ret.wheelSpeeds.fr = cp.vl[CAN.WHEEL_SPEEDS]['WHEEL_SPEED_FR'] * 0.01
        ret.vEgo = (ret.wheelSpeeds.fl + ret.wheelSpeeds.fr) / 2.0
        
        # Estado do Volante (ID 0x1ab)
        ret.steeringAngleDeg = cp.vl[CAN.ADAS_STATUS]['STEER_ANGLE']
        ret.steeringPressed = abs(cp.vl[CAN.ADAS_STATUS]['STEER_TORQUE_SENSOR']) > 50

        return ret

    @staticmethod
    def get_can_parser(CP):
        # Aqui definimos quais IDs o parser deve "escutar"
        messages = [
            (CAN.WHEEL_SPEEDS, 50),
            (CAN.ADAS_STATUS, 100),
            (CAN.GAS_PEDAL, 100),
        ]
        return CANParser("renault_megane_etech", messages, 0) # 0 é o bus da câmera
