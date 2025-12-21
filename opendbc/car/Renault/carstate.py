from opendbc.can.parser import CANParser
from opendbc.car.interfaces import CarStateBase
from opendbc.car.renault.values import CAR, CAN
from common.conversions import Conversions as CV # Importante para m/s

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

  def update(self, cp):
    ret = CarStateBase.new_message()

    # --- 1. VELOCIDADE E RODAS (Mesclado com CV) ---
    # Multiplicamos pelo fator do DBC (0.01) e convertemos para Metros por Segundo
    ret.wheelSpeeds.fl = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_FL"] * 0.01 * CV.KPH_TO_MS
    ret.wheelSpeeds.fr = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_FR"] * 0.01 * CV.KPH_TO_MS
    ret.wheelSpeeds.rl = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_RL"] * 0.01 * CV.KPH_TO_MS
    ret.wheelSpeeds.rr = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_RR"] * 0.01 * CV.KPH_TO_MS
    
    # Média das 4 rodas em m/s
    ret.vEgo = (ret.wheelSpeeds.fl + ret.wheelSpeeds.fr + ret.wheelSpeeds.rl + ret.wheelSpeeds.rr) / 4.0
    ret.vEgoRaw = ret.vEgo
    
    # Standstill: Usamos o bit do DBC se disponível, ou a velocidade < 0.1 m/s
    ret.standstill = cp.vl["ADAS_CAM_MISC"]["STANDSTILL"] == 1 or ret.vEgoRaw < 0.1

    # --- 2. DIREÇÃO ---
    ret.steeringAngleDeg = cp.vl["ADAS_STATUS"]["STEER_ANGLE"]
    ret.steeringRateDeg = cp.vl["ADAS_STATUS"]["STEER_RATE"]
    ret.steeringTorque = cp.vl["ADAS_STATUS"]["STEER_TORQUE_SENSOR"]
    ret.steeringPressed = abs(ret.steeringTorque) > 50 

    # --- 3. ACELERADOR E TRAVÃO (Sinais Reais do DBC) ---
    ret.gas = cp.vl["GAS_PEDAL"]["GAS_PEDAL_POS"] / 100.0
    ret.gasPressed = ret.gas > 1e-5
    ret.brakePressed = cp.vl["BRAKE_STATE"]["BRAKE_PRESSED"] == 1

    # --- 4. SEGURANÇA (Obrigatório para o OpenPilot) ---
    ret.seatbeltUnlatched = cp.vl["CAR_STATE_SIGNALS"]["SEATBELT_DRIVER"] == 0
    ret.doorOpen = cp.vl["CAR_STATE_SIGNALS"]["DOOR_OPEN_DRIVER"] == 1

    # --- 5. CRUISE CONTROL (Mapeado do ADAS) ---
    ret.cruiseState.enabled = cp.vl["ADAS_CAM_STATE"]["ACC_ACTIVE"] == 1
    ret.cruiseState.available = True 

    return ret

  @staticmethod
  def get_can_parser(CP):
    # Lista de mensagens que o parser deve ler do DBC
    messages = [
      ("ADAS_STATUS", 100),
      ("WHEEL_SPEEDS", 50),
      ("GAS_PEDAL", 50),
      ("BRAKE_STATE", 50),
      ("CAR_STATE_SIGNALS", 10),
      ("ADAS_CAM_STATE", 20),
      ("ADAS_CAM_MISC", 10),
    ]

    return CANParser("megane_etech", messages, 0)
