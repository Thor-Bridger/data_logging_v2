"""Main application to read and display SHT30 sensor data once."""

import sht30_sensor
import DS18B20_sensor
import fl808_sensor
import time

def print_ds18b20_readings(temperatures):
    """Prints the DS18B20 temperature readings."""
    print("\n--- DS18B20 Temperature Readings ---")
    if temperatures:
        for idx, temp in enumerate(temperatures):
            print(f"Sensor {idx + 1}: {temp:.2f} °C")
    else:
        print("No DS18B20 sensors found or failed to read data.")
def print_sht30_reading(sht30_data):
    """Prints the SHT30 sensor reading."""
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

if __name__ == "__main__":
    start_time = time.time()
    
    # Read and print DS18B20 temperatures
    ds18b20_temps = DS18B20_sensor.read_temperature()
    print_ds18b20_readings(ds18b20_temps)

    # Read and print SHT30 data
    sht30_data = sht30_sensor.read_once()
    print_sht30_reading(sht30_data)

    # Read and print FL808 sensor toggle count
    print("\n--- FL808 Sensor Reading ---")

    try:
            fl808_sensor.watch_line_rising("/dev/gpiochip0", 5)
    
    except OSError as ex:
        print(ex, "\nCustomise the example configuration to suit your situation")
    
    print(f"\nTotal execution time: {time.time() - start_time:.2f} seconds")







