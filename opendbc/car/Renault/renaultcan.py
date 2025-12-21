def renault_checksum(address: int, sig, d: bytearray) -> int:
    # O Megane usa CRC8 Autosar (Polinômio 0x1D)
    # No seu log, vimos que o Checksum está no byte 4. 
    # Geralmente calcula-se sobre todos os bytes exceto o próprio byte de checksum.
    crc = 0xFF
    poly = 0x1D

    for i, b in enumerate(d):
        if i == 4: # Pula o byte onde o Checksum será gravado
            continue
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc <<= 1
    return crc ^ 0xFF


def create_steering_control(packer, torque, counter):
    """
    Cria a mensagem de controle de torque (substituindo o helloworld do GWM)
    """
    values = {
        'STEER_TORQUE': torque,
        'COUNTER': counter,
    }
    
    # 1. O packer monta a mensagem baseada no seu megane_etech.dbc
    # Retorna (address, bus, data, length)
    _, _, dat, _ = packer.make_can_msg('ADAS_STATUS', 0, values)
    
    # 2. Calculamos o Checksum sobre os dados gerados
    values['CHECKSUM'] = renault_checksum(0x1ab, None, dat)
    
    # 3. Retornamos a mensagem final completa
    return packer.make_can_msg('ADAS_STATUS', 0, values)
