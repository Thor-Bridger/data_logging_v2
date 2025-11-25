"""Main application to read and display SHT30 sensor data once."""

from sht30_sensor import read_once
from DS18B20_sensor import read_temperature

if __name__ == "__main__":
    sht30_data = read_once()
    ds18b20_temps = read_temperature()

    print("\n--- DS18B20 Temperature Readings ---")
    if ds18b20_temps:
        for idx, temp in enumerate(ds18b20_temps):
            print(f"Sensor {idx + 1}: {temp:.2f} °C")
    else:
        print("No DS18B20 sensors found or failed to read data.")
    
    print("\n--- SHT30 Sensor Reading ---")
    if sht30_data:
        temp_c, hum_pct = sht30_data
        
        # Print the data in the requested format
        print("\n--- Current Reading ---")
        print(f"Temperature: {temp_c:.2f} °C")
        print(f"Humidity:    {hum_pct:.2f} %")
    else:
        print("\nFailed to get a reading from the sensor.")
        print("Check `sht30_sensor.py` output for initialization errors.")
        
    print("-------------------------")







