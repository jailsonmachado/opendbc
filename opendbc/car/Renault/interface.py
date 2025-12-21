from cereal import car
from opendbc.car import get_safety_config
from opendbc.car.interfaces import CarInterfaceBase
from opendbc.car.renault.values import CAR

class CarInterface(CarInterfaceBase):
    @staticmethod
    def get_params(candidate, fingerprint=None, car_fw=None, experimental_long=False, docs=False):
        ret = CarInterfaceBase.get_std_params(candidate, fingerprint)
        ret.carName = "renault"
        
        # Configuração de Segurança (Safety Model)
        # Usamos Nissan como base de barramento para o Panda
        ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.nissan)]
        
        # Parâmetros físicos específicos do Megane E-Tech
        if candidate == CAR.MEGANE_ETECH:
            ret.mass = 1708.        # kg
            ret.wheelbase = 2.68    # metros
            ret.steerRatio = 14.5   # Relação de direção
            ret.centerToFront = ret.wheelbase * 0.44
            
        # Tempos de resposta do atuador
        ret.steerActuatorDelay = 0.1
        ret.steerLimitTimer = 0.4
        
        # Habilita o suporte obrigatório para as mensagens longas (48/64 bytes) do Megane
        ret.flags |= car.CarParams.Flags.CANFD

        return ret

    # Método que faz a ponte com o CarController para enviar os comandos
    def apply(self, c, now_nanos):
        return self.CC.update(c, self.CS, now_nanos)
