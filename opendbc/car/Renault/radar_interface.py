from opendbc.car.interfaces import RadarInterfaceBase

class RadarInterface(RadarInterfaceBase):
  def __init__(self, CP):
    super().__init__(CP)
    # Renault Megane E-Tech utiliza radar integrado à câmera ou via CAN-FD 
    # que o OpenPilot processa como 'Empty' se não houver radar externo.
    self.updated_messages = set()

  def update(self, can_strings):
    return None
