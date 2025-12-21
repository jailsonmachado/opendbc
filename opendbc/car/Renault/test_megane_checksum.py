def renault_checksum(data: bytearray) -> int:
    # Algoritmo que definimos para o Megane (CRC8 Autosar)
    crc = 0xFF
    poly = 0x1D
    for i, b in enumerate(data):
        if i == 4: continue # O byte 4 é onde o checksum vive, então pulamos ele
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc <<= 1
    return crc ^ 0xFF

# --- TESTE COM DADOS REAIS DO SEU LOG ---
# Peguei uma linha aproximada do seu log anterior (48 bytes)
# O byte index 4 (o 5º byte) é o Checksum original.
messages_to_test = [
    # Substitua abaixo por sequências hexadecimais REAIS do seu arquivo .csv
    # Formato: bytearray.fromhex("00 11 22 33 CHECKSUM 55 ...")
    "023101006500000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
]

print("=== VALIDANDO CHECKSUM RENAULT MEGANE CAN-FD ===")
for hex_str in messages_to_test:
    msg = bytearray.fromhex(hex_str)
    original_checksum = msg[4]
    
    calculated = renault_checksum(msg)
    
    match = "✓ PASSOU" if calculated == original_checksum else "✗ FALHOU"
    
    print(f"\nDados: {hex_str[:20]}...")
    print(f"Original no Log: 0x{original_checksum:02X}")
    print(f"Calculado pelo Script: 0x{calculated:02X}")
    print(f"Resultado: {match}")
