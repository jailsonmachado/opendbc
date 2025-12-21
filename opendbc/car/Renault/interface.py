from car.renault.values import CAR
from car import get_safety_config
from car.interfaces import CarInterfaceBase

class CarInterface(CarInterfaceBase):
    @staticmethod
    def get_params(candidate, fingerprint=None, car_fw=None, experimental_long=False):
        ret = CarInterfaceBase.get_std_params(candidate, fingerprint)
        ret.carName = "renault"
        
        # Configuração de Segurança (Safety Model)
        # Inicialmente usamos o da Nissan porque o Checksum é quase idêntico
        ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.nissan)]
        
        ret.steerActuatorDelay = 0.1
        ret.steerLimitTimer = 0.4
        
        return ret
