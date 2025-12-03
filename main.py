"""Main application to read and display SHT30 sensor data once."""

import i2c_sensors
import DS18B20_sensor
import fl808_sensor
import time

def print_ds18b20_readings(temperatures, ids):
    """Prints the DS18B20 temperature readings."""
    print("\n--- DS18B20 Temperature Readings ---")
    if temperatures and ids and (len(temperatures) == len(ids)): # Minimal change: ensure lists are valid
        # FIX: Use zip() to iterate over both lists simultaneously
        for idx, (temp, id) in enumerate(zip(temperatures, ids)): 
            print(f"Sensor {idx + 1}({id}): {temp:.2f} °C")
    else:
        # Minimal change: print a more informative message if lists don't match or are empty
        print("No DS18B20 sensors found or failed to read data/match IDs.")

def print_sht30_reading(sht30_data):
    """Prints readings for all detected SHT30 sensors."""
    print("\n--- SHT30 Sensor Readings ---")
    for idx, (temp, hum) in enumerate(sht30_data):
        if temp is not None and hum is not None:
            print(f"SHT30 Sensor {idx + 1}: Temperature: {temp:.2f} °C, Humidity: {hum:.2f} %")
        else:
            print(f"SHT30 Sensor {idx + 1}: Read failed or sensor not detected.")
    
    
def main():
    start_time = time.time()

    while(True):
    
        # Read and print DS18B20 temperatures
        ds18b20_temps, db18b20_ids = DS18B20_sensor.read_temperature()
        print_ds18b20_readings(ds18b20_temps, db18b20_ids)

        # Read and print SHT30 data
        sht30_data = i2c_sensors.read_all_sensors(0x44)
        print_sht30_reading(sht30_data)

        #Read and print MS4525 pressure data
        print("\n--- MS4525 Pressure Readings ---")
        ms4525_data = i2c_sensors.read_all_sensors(0x00)  # Test address for MS4525
        print(f"MS4525 Sensor 1 (bus1): {ms4525_data[0][0]} Pa \nTemperature: {ms4525_data[0][1]} °C")
        
        # Read and print FL808 sensor toggle count
        fl808_data = fl808_sensor.watch_line_rising("/dev/gpiochip0", 5)
        print("\n--- FL808 Sensor Data ---")
        print(f"Fow Rate: {fl808_data} L/min")
        
        

        try:
            pass
                #fl808_sensor.watch_line_rising("/dev/gpiochip0", 5)
        
        except OSError as ex:
            print(ex, "\nCustomise the example configuration to suit your situation")
        
        print(f"\nTotal execution time: {time.time() - start_time:.2f} seconds")


main()    







