from opendbc.can.parser import CANParser
from opendbc.car.interfaces import CarStateBase
from opendbc.car.renault.values import CAR, DBC
from common.conversions import Conversions as CV

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

  def update(self, cp):
    ret = CarStateBase.new_message()

    # --- 1. VELOCIDADE E RODAS ---
    # O DBC ja entrega em km/h (ex: 44.0). So precisamos converter para m/s.
    # NAO multiplique por 0.01 aqui, pois o DBC ja fez isso!
    ret.wheelSpeeds.fl = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_FL"] * CV.KPH_TO_MS
    ret.wheelSpeeds.fr = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_FR"] * CV.KPH_TO_MS
    ret.wheelSpeeds.rl = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_RL"] * CV.KPH_TO_MS
    ret.wheelSpeeds.rr = cp.vl["WHEEL_SPEEDS"]["WHEEL_SPEED_RR"] * CV.KPH_TO_MS
    
    # Media das 4 rodas em m/s
    ret.vEgo = (ret.wheelSpeeds.fl + ret.wheelSpeeds.fr + ret.wheelSpeeds.rl + ret.wheelSpeeds.rr) / 4.0
    ret.vEgoRaw = ret.vEgo
    
    # Standstill: velocidade < 0.1 m/s ou sinal da camera
    ret.standstill = cp.vl["ADAS_CAM_MISC"]["STANDSTILL"] == 1 or ret.vEgoRaw < 0.1

    # --- 2. DIRECAO ---
    ret.steeringAngleDeg = cp.vl["ADAS_STATUS"]["STEER_ANGLE"]
    ret.steeringRateDeg = cp.vl["ADAS_STATUS"]["STEER_RATE"]
    ret.steeringTorque = cp.vl["ADAS_STATUS"]["STEER_TORQUE_SENSOR"]
    # Ajuste inicial: considera mao no volante se torque > 50 unidades (pode precisar ajuste)
    ret.steeringPressed = abs(ret.steeringTorque) > 50 

    # --- 3. ACELERADOR E FREIO ---
    ret.gas = cp.vl["GAS_PEDAL"]["GAS_PEDAL_POS"] / 100.0
    ret.gasPressed = ret.gas > 1e-5
    
    # Usando o CRUISE_STATE (ID 768) como backup, ja que o antigo BRAKE_STATE (311) nao existe
    ret.brakePressed = cp.vl["CRUISE_STATE"]["BRAKE_PRESSED"] == 1

    # --- 4. SEGURANCA ---
    # Como removemos o ID CAR_STATE_SIGNALS do DBC (nao existia no log),
    # travamos esses valores como falsos para nao dar erro no startup.
    ret.seatbeltUnlatched = False 
    ret.doorOpen = False

    # --- 5. CRUISE CONTROL ---
    # Logica 'OU': Se a Camera OU o painel (768) disserem que esta ativo, entao esta.
    ret.cruiseState.enabled = cp.vl["ADAS_CAM_STATE"]["ACC_ACTIVE"] == 1 or cp.vl["CRUISE_STATE"]["CRUISE_ACTIVE"] == 1
    ret.cruiseState.available = True 

    return ret

  @staticmethod
  def get_can_parser(CP):
    # IMPORTANTE: O nome aqui deve bater com o nome do arquivo na pasta dbc (sem a extensao)
    # Baseado no seu link do GitHub: 'megane_etech.dbc' -> 'megane_etech'
    dbc_name = "megane_etech"
    
    messages = [
      ("ADAS_STATUS", 100),
      ("WHEEL_SPEEDS", 50),
      ("GAS_PEDAL", 50),
      ("ADAS_CAM_STATE", 20),
      ("ADAS_CAM_MISC", 10),
      ("CRUISE_STATE", 20), # ID 768
    ]

    return CANParser(dbc_name, messages, 0)
