from opendbc.can.packer import CANPacker
from opendbc.car import Bus, structs
from opendbc.car.interfaces import CarControllerBase
# Importamos a função que você criou para não repetir código
from opendbc.can.renaultcan import renault_checksum 

class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.main])
    self.frame = 0

  def update(self, CC, CS, now_nanos):
    actuators = CC.actuators
    can_sends = []

    # 1. Lógica de Torque (Aproveitada do início)
    # actuators.steer varia de -1 a 1. Multiplicamos pelo torque máximo.
    apply_torque = 0
    if CC.enabled:
      apply_torque = int(round(actuators.steer * 300)) # 300 é um valor inicial seguro

    # 2. Preparar valores para o Packer (Baseado no seu DBC)
    # O Contador gira de 0 a 15 (self.frame % 16)
    counter = self.frame % 16
    
    values = {
      "STEER_TORQUE": apply_torque,
      "COUNTER": counter,
    }

    # 3. Gerar Checksum (Aproveitado do início)
    # Primeiro geramos a mensagem "vazia" de checksum para pegar os bytes
    _, _, dat, _ = self.packer.make_can_msg("ADAS_STATUS", 0, values)
    
    # Calculamos o Checksum sobre os bytes (como você fez no dat[5:12])
    # A função renault_checksum já ignora o byte 4 (onde o próprio chk fica)
    values["CHECKSUM"] = renault_checksum(0x1ab, None, dat)

    # 4. Adicionar à lista de envio
    can_sends.append(self.packer.make_can_msg("ADAS_STATUS", 0, values))

    self.frame += 1
    
    # Retorno padrão exigido pela estrutura nova (structs)
    new_actuators = actuators.as_builder()
    return new_actuators, can_sends
