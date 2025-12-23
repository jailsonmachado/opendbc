import crcmod

def test_checksum():
    print("=== TESTE DE CHECKSUM MEGANE E-TECH ===")
    
    # Dados reais do seu log (ID 0x1ab)
    # Payload: 00 00 FF 06 82 B1 FE 96 ... (Checksum é 0x82)
    raw_hex = "0000FF0682B1FE96FFFA0000B4086CB07D47D47C77CA0000AB08B9B3E800FFFE7D000000000000000000000000000000"
    data = bytearray.fromhex(raw_hex)
    
    original_crc = data[4] # 0x82
    print(f"Checksum Original no Log: 0x{original_crc:02X}")

    # TENTATIVA 1: Autosar Padrão (0x1D)
    try:
        autosar_crc = crcmod.mkCrcFun(0x11D, initCrc=0xFF, rev=False, xorOut=0xFF)
        # Pula byte 4
        payload = data[0:4] + data[5:]
        calc = autosar_crc(payload)
        print(f"Calculado (Poly 0x1D): 0x{calc:02X} -> {'SUCESSO' if calc == original_crc else 'FALHA'}")
    except ImportError:
        print("Erro: Instale crcmod (pip install crcmod)")

    # TENTATIVA 2: Nissan Novo (0x2F)
    try:
        nissan_crc = crcmod.mkCrcFun(0x12F, initCrc=0xFF, rev=False, xorOut=0xFF)
        payload = data[0:4] + data[5:]
        calc = nissan_crc(payload)
        print(f"Calculado (Poly 0x2F): 0x{calc:02X} -> {'SUCESSO' if calc == original_crc else 'FALHA'}")
    except:
        pass

if __name__ == "__main__":
    test_checksum()
