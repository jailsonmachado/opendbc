from opendbc.car import structs, get_safety_config
from opendbc.car.interfaces import CarInterfaceBase
from opendbc.car.renault.carcontroller import CarController
from opendbc.car.renault.carstate import CarState
from opendbc.car.renault.values import CAR

# Atalho para facilitar a leitura
CarParams = structs.CarParams

class CarInterface(CarInterfaceBase):
  CarState = CarState
  CarController = CarController

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, alpha_long, is_release, docs) -> structs.CarParams:
    ret.brand = 'renault'

    # Modelo de segurança. Inicialmente usamos Nissan para CAN-FD, 
    # pois o suporte Renault CAN-FD no Panda é derivado dele.
    ret.safetyConfigs = [get_safety_config(CarParams.SafetyModel.nissan)]

    # Habilita o suporte a CAN-FD (Crucial para Megane E-Tech)
    ret.flags |= CarParams.Flags.CANFD.value

    # Configurações de Direção
    ret.steerActuatorDelay = 0.1  # Megane responde rápido
    ret.steerLimitTimer = 0.4
    ret.steerAtStandstill = True

    # Definimos como torque, pois o Megane (via câmera) recebe comandos de torque
    ret.steerControlType = CarParams.SteerControlType.torque

    # Dados físicos da plataforma CMF-EV (Megane)
    if candidate == CAR.MEGANE_ETECH:
      ret.mass = 1708.
      ret.wheelbase = 2.68
      ret.steerRatio = 14.5
      ret.centerToFront = ret.wheelbase * 0.44

    return ret
