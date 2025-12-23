import crcmod
from opendbc.car.renault.values import CAR

# Configuração do CRC Autosar (Padrão mais provável para Megane E-Tech)
# Poly 0x1D, Init 0xFF, XorOut 0xFF
renault_checksum = crcmod.mkCrcFun(0x11D, initCrc=0xFF, rev=False, xorOut=0xFF)

def create_steering_control(packer, steer_idx, steer_torq, steer_angle):
  # Prepara os valores para o pacote
  # ATENÇÃO: Os nomes das chaves DEVEM bater com o seu DBC 'megane_etech.dbc'
  values = {
    "COUNTER": steer_idx % 16,
    "STEER_TORQUE_SENSOR": steer_torq,  # Corrigido de 'STEER_TORQUE'
    "STEER_ANGLE": steer_angle,         # Enviar o angulo atual ajuda na aceitacao
    "CHECKSUM": 0,                      # Zera para calcular
  }
  
  # 1. Cria a mensagem bruta (dat)
  # O ID 427 em decimal é 0x1ab
  # O packer retorna (addr, bus, dat, len) -> Pegamos o [2] que é o dado
  dat = packer.make_can_msg("ADAS_STATUS", 0, values)[2]
  
  # 2. Calcula o CRC
  # A lógica Autosar pula o byte do CRC. No seu DBC, CRC está no Byte 4.
  # dat[0:4] + dat[5:] remove o byte 4 do cálculo.
  crc = renault_checksum(dat[0:4] + dat[5:])
  
  # 3. Insere o CRC calculado e monta a mensagem final
  values["CHECKSUM"] = crc
  return packer.make_can_msg("ADAS_STATUS", 0, values)
