def convert_SHT30(raw_temp, raw_hum):
    """Convert raw SHT30 sensor data to temperature (°C) and humidity (%RH)."""
    if raw_temp is None or raw_hum is None:
        return None, None

    # Temperature conversion formula from SHT30 datasheet
    temperature = -45 + (175 * (raw_temp / 65535.0))
    
    # Humidity conversion formula from SHT30 datasheet
    humidity = 100 * (raw_hum / 65535.0)
    
    return temperature, humidity

def convert_MS4525(raw_pressure, raw_temperature):
    """
    Convert raw MS4525DO data to Pascals (Pa) and Temperature (°C).
    Assumes standard 1 PSI Differential Airspeed Sensor (-1 to +1 psi).
    """
    if raw_pressure is None or raw_temperature is None:
        return None, None

    # --- CONSTANTS ---
    # 1 PSI = 6894.76 Pascals
    # Standard Airspeed sensor range is -1 PSI to +1 PSI
    P_MIN_PA = -6894.76
    P_MAX_PA = 6894.76
    
    # 1. Mask out Status Bits
    # Pressure is 14-bit (mask 0x3FFF), Temperature is 11-bit (mask 0x07FF)
    p_data = raw_pressure & 0x3FFF
    t_data = raw_temperature & 0x07FF

    # 2. Calculate Pressure in Pascals
    # Based on 10% to 90% transfer function (1638 to 14745 counts)
    # Range of counts = 14745 - 1638 = 13107
    psi_span = P_MAX_PA - P_MIN_PA
    pressure = ((p_data - 1638) * psi_span) / 13107 + P_MIN_PA

    # 3. Calculate Temperature in Celsius
    # Standard formula: T = (Counts * 200 / 2047) - 50
    temperature = (t_data * 200.0 / 2047.0) - 50.0

    return pressure, temperature
