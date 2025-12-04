# sht30_sensor.py

import smbus2
import time
from typing import Optional, List
from smbus2 import i2c_msg
import queue
import threading

# I2C Bus Number (1 for the 40-pin header on all recent Pis)
I2C_BUS_ID = 1

# Commands for the SHT30 sensor 
# 0x2400: High repeatability, Clock stretching disabled (poll for result)
# 0x2C06: High repeatability, Clock stretching disabled (alternative command)
SHT30_MEASURE_CMD = [0x24, 0x00]

bus1 = smbus2.SMBus(1)  # The standard pins
bus3 = smbus2.SMBus(3)  # The new virtual pins defined in config.txt
time.sleep(0.1)  # Short delay to ensure bus is ready


# --- Initialization ---
try:
    bus = smbus2.SMBus(I2C_BUS_ID)
    print("SHT30 Sensor: I2C bus initialized successfully with smbus2.")
except Exception as e:
    print(f"SHT30 Sensor Error: Failed to initialize I2C bus: {e}")
    bus = None 

def read_sht30(bus, address) -> Optional[tuple[float, float]]:
    """
    Reads a specific SHT30 sensor based on the provided I2C address.
    Returns: (temperature_celsius, humidity_percent) or None on failure.
    """
    if bus is None:
        return None

    try:
        # 1. Send the measure command to the specific address
        bus.write_i2c_block_data(address, SHT30_MEASURE_CMD[0], [SHT30_MEASURE_CMD[1]])
        
        # 2. Wait for the measurement to complete (High precision takes ~15ms)
        time.sleep(0.02) 

        # 3. Read the 6 bytes of data from the specific address
        data = bus.read_i2c_block_data(address, 0x00, 16)
        
        # 4. Convert the raw data to temperature and humidity
        
        # Temperature conversion
        raw_temp = (data[0] << 8) | data[1]

        # Humidity conversion
        raw_hum = (data[3] << 8) | data[4]

        # Return formatted tuple
        return (raw_temp, raw_hum)
    
    except Exception as e:
        pass
        #print(e)
     
        return None
    
def read_ms4525(bus, address) -> Optional[float]:
    """
    Reads a specific MS4525 sensor based on the provided I2C address.
    Returns: pressure in Pascals or None on failure.
    """
    if bus is None:
        print('MS4525 Sensor: I2C bus not initialized.')
        return None

    try:
        # 1. Read 4 bytes of data from the specific address
        #print("Searching address:", hex(add))

        #data = i2c_msg.read(address, 4) # Wake up
        #time.sleep(0.1)

        data = i2c_msg.read(address, 4) # Actual read
        bus.i2c_rdwr(data)

        found_data = list(data)
        #print("Data from address", hex(address), ":", found_data)

        # 2. Convert the raw data to pressure
        raw_pressure = (found_data[0] << 8) | found_data[1]

        # 3. Convert raw temperature
        raw_temp = (found_data[2] << 3) | (found_data[3] >> 5)


        return [raw_pressure, raw_temp]
    
    except Exception as e:
        # Uncomment the line below for debugging specific sensor failures
        # print(f"Failed to read address {hex(address)}: {e}")
        return None


def read_all_sensors(address) -> List[List[float]]:
    results = []
    if address is 0x44: # Standard SHT30 address
        results.append(read_sht30(bus1, address) or [None, None])  # Sensor on bus1 at address 0x44
        results.append(read_sht30(bus3, address) or [None, None]) # Sensor on bus3 at address 0x44

    else:
        results.append(read_ms4525(bus1, address) or None)  # Sensor on bus1 at other address

        pass

    return results


def i2c_read_thread(sht30_queue, ms4525_queue):
    while True:
        try:
            sht30_queue.put(read_all_sensors(0x44))  # SHT30 address
            ms4525_queue.put(read_all_sensors(0xa8))  # MS452
            
        except KeyboardInterrupt:
            break


