from math import sqrt, exp


def convert_SHT30(raw_temp, raw_hum):
    """Convert raw SHT30 sensor data to temperature (°C) and humidity (%RH)."""
    if raw_temp is None or raw_hum is None:
        return None, None

    # Temperature conversion formula from SHT30 datasheet
    temperature = -45 + (175 * (raw_temp / 65535.0))
    
    # Humidity conversion formula from SHT30 datasheet
    humidity = 100 * (raw_hum / 65535.0)
    
    return temperature, humidity

def convert_MS4525(raw_pressure, raw_temperature, humidity=50.0):
    """
    Convert MS4525DO-DS5A001DP (1 PSI Differential) data to Pa, °C, and m/s.
    
    Args:
        raw_pressure (int): Raw 14-bit pressure value.
        raw_temperature (int): Raw 11-bit temperature value.
        humidity (float): SHT30 Humidity % (defaults to 50% if missing).
    
    Returns:
        tuple: (Pressure_Pa, Temperature_C, Airspeed_m_s)
    """
    if raw_pressure is None or raw_temperature is None:
        return None, None, None

    # --- 1. SENSOR CONSTANTS (MS4525DO-DS5A001DP) ---
    P_MIN_PSI = -1.0
    P_MAX_PSI = 1.0
    PSI_TO_PA = 6894.76
    
    # Type A Transfer Function limits (14-bit)
    # 10% = 1638 counts, 90% = 14745 counts
    COUNTS_MIN = 1638.3
    COUNTS_SPAN = 13106.4  # (90% - 10%) of 16383

    # --- 2. DECODE DATA ---
    # Mask status bits (top 2 bits)
    p_data = raw_pressure & 0x3FFF
    t_data = raw_temperature & 0x07FF

    # --- 3. PRESSURE CONVERSION ---
    # Formula: P_applied = P_min + ( (Output - 10%Counts) * (P_max - P_min) / 80%Counts )
    
    psi_range = P_MAX_PSI - P_MIN_PSI # Range is 2.0 psi (-1 to +1)
    
    pressure_psi = P_MIN_PSI + ((p_data - COUNTS_MIN) * psi_range / COUNTS_SPAN)
    
    # Convert to Pascals (Pa)
    pressure_pa = pressure_psi * PSI_TO_PA

    # --- 4. TEMPERATURE CONVERSION ---
    # Formula: T(°C) = (Counts * 200 / 2047) - 50
    temp_c = (t_data * 200.0 / 2047.0) - 50.0

    # --- 5. AIRSPEED CALCULATION (with Density Correction) ---
    # Physics constants
    Rd = 287.05   # Dry air constant
    Rv = 461.495  # Water vapor constant
    P_STATIC = 101325.0 # Standard sea level pressure (Pa)
    temp_k = temp_c + 273.15

    # Saturation Vapor Pressure (Tetens Equation)
    eso = 6.1078 * exp((17.27 * temp_c) / (temp_c + 237.3)) * 100
    
    # Partial Vapor Pressure
    pv = eso * (humidity / 100.0)
    
    # Partial Dry Air Pressure
    pd = P_STATIC - pv

    # Air Density (rho)
    density = (pd / (Rd * temp_k)) + (pv / (Rv * temp_k))

    # Bernoulli Equation: V = sqrt(2 * DynamicPressure / Density)
    # 1. We take absolute value because noise near 0 can trigger negative numbers.
    # 2. In a real pitot tube, negative pressure usually means wind blowing backwards 
    #    or installation error, but we treat it as 0 speed for safety.
    if pressure_pa <= 0:
        wind_speed = 0.0
    else:
        wind_speed = sqrt((2 * pressure_pa) / density)

    return pressure_pa, temp_c, wind_speed

