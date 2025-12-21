from opendbc.can.parser import CANParser
from common.conversions import Conversions as CV
from selfdrive.car.interfaces import CarStateBase
from selfdrive.car.renault.values import CAN

class CarState(CarStateBase):
    def __init__(self, CP):
        super().__init__(CP)
        # Inicializa variáveis de estado se necessário

    def update(self, cp):
        ret = CarStateBase.new_message()

        # 1. Velocidade do Veículo (vEgo)
        # Usamos a média das rodas frontais (ID 0x226 no teu log)
        # O fator 0.01 foi estimado; se a velocidade no ecrã do OP estiver errada, ajustamos aqui.
        ret.wheelSpeeds.fl = cp.vl[CAN.WHEEL_SPEEDS]['WHEEL_SPEED_FL'] * 0.01 * CV.KPH_TO_MS
        ret.wheelSpeeds.fr = cp.vl[CAN.WHEEL_SPEEDS]['WHEEL_SPEED_FR'] * 0.01 * CV.KPH_TO_MS
        ret.vEgo = (ret.wheelSpeeds.fl + ret.wheelSpeeds.fr) / 2.0
        ret.vEgoRaw = ret.vEgo
        ret.standstill = ret.vEgoRaw < 0.1

        # 2. Direção (Ângulo e Torque)
        # Retirado do ID 0x1ab (48 bytes) que vimos no log
        ret.steeringAngleDeg = cp.vl[CAN.ADAS_STATUS]['STEER_ANGLE']
        ret.steeringRateDeg = 0.0 # Pode ser calculado se necessário
        
        # Torque aplicado pelo condutor (para saber se as mãos estão no volante)
        ret.steeringTorque = cp.vl[CAN.ADAS_STATUS]['STEER_TORQUE_SENSOR']
        ret.steeringPressed = abs(ret.steeringTorque) > 50 # Limiar de detecção de mãos

        # 3. Acelerador
        # ID 0x303 (GAS_PEDAL)
        ret.gas = cp.vl[CAN.GAS_PEDAL]['GAS_PEDAL_POS'] / 100.0
        ret.gasPressed = ret.gas > 1e-5

        # 4. Cruise Control e Travão (Stock)
        # Nota: Estes IDs ainda precisam de ser confirmados quando tiveres o hardware,
        # pois geralmente exigem que o Cruise Control esteja ligado para aparecerem.
        ret.brakePressed = False # TODO: Mapear ID do travão
        ret.cruiseState.enabled = True # Forçamos para testes, mas deve vir da rede CAN
        ret.cruiseState.available = True

        return ret

    @staticmethod
    def get_can_parser(CP):
        # Aqui definimos quais as mensagens que o openpilot deve "vigiar" na rede
        messages = [
            # ID, Frequência (Hz)
            (CAN.ADAS_STATUS, 100),
            (CAN.WHEEL_SPEEDS, 50),
            (CAN.GAS_PEDAL, 100),
        ]

        # O nome "megane_etech" deve ser igual ao nome do teu ficheiro .dbc
        return CANParser("megane_etech", messages, 0)
