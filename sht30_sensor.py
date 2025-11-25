# sht30_sensor.py

import smbus2
import time
from typing import Optional

# I2C Bus Number (1 for the 40-pin header on all recent Pis)
I2C_BUS_ID = 1
# Default I2C address for the SHT30
I2C_ADDRESS = 0x44 

# Commands for the SHT30 sensor (Measure High Precision)
SHT30_MEASURE_CMD = [0x24, 0x00] # Single shot, high repeatability

# --- Initialization ---
try:
    # Initialize the I2C bus object
    bus = smbus2.SMBus(I2C_BUS_ID)
    print("SHT30 Sensor: I2C bus initialized successfully with smbus2.")
except Exception as e:
    print(f"SHT30 Sensor Error: Failed to initialize I2C bus: {e}")
    bus = None 

def _check_crc(data: bytes, crc: int) -> bool:
    """Helper to check the 8-bit CRC for SHT30 data."""
    # CRC checking is important but omitted here for simplicity and readability 
    # as per your request. The raw read is more direct.
    # In production code, you would implement the CRC check here.
    return True # Simple version: assume CRC is correct

def read_once() -> Optional[tuple[float, float]]:
    """
    Reads the SHT30 sensor directly via I2C commands.
    Returns: (temperature_celsius, humidity_percent) or None on failure.
    """
    if bus is None:
        return None

    try:
        # 1. Send the measure command
        bus.write_i2c_block_data(I2C_ADDRESS, SHT30_MEASURE_CMD[0], [SHT30_MEASURE_CMD[1]])
        
        # 2. Wait for the measurement to complete (High precision takes ~15ms)
        time.sleep(0.02) 

        # 3. Read the 6 bytes of data (Temp MSB, Temp LSB, Temp CRC, Hum MSB, Hum LSB, Hum CRC)
        data = bus.read_i2c_block_data(I2C_ADDRESS, 0x00, 6)
        
        # 4. Convert the raw data to temperature and humidity

        # Temperature conversion
        raw_temp = (data[0] << 8) | data[1]
        temp_c = -45 + (175 * raw_temp / 65535.0)

        # Humidity conversion
        raw_hum = (data[3] << 8) | data[4]
        hum_pct = (100 * raw_hum / 65535.0)

        # 5. Check CRC (omitted for simple code, but normally done here with data[2] and data[5])
        
        return (temp_c, hum_pct)
    
    except Exception as e:
        print(f"SHT30 Sensor Read Error: {e}")
        return None