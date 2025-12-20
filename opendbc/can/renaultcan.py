def renault_checksum(addr, sig, data):
  crc = 0xFF
  poly = 0x1D
  for i in range(len(data)):
    if i == 4: continue 
    crc ^= data[i]
    for _ in range(8):
      if crc & 0x80:
        crc = ((crc << 1) ^ poly) & 0xFF
      else:
        crc <<= 1
  return crc ^ 0xFF
