"""Main application to read and display SHT30 sensor data once."""

import i2c_sensors
import DS18B20_sensor
import fl808_sensor
import conversions
import logging

import time
import queue
import threading


def main():
    # Create queues for inter-thread communication
    ds18b20_queue = queue.Queue()
    sht30_queue = queue.Queue()
    ms4525_queue = queue.Queue()
    fl808_queue = queue.Queue()

    # Start I2C reading thread
    i2c_read_thread = threading.Thread(target=i2c_sensors.i2c_read_thread, args=(sht30_queue, ms4525_queue))
    i2c_read_thread.start()

    # Start DS18B20 reading thread
    ds18b20_thread = threading.Thread(target=DS18B20_sensor.one_wire_read_thread, args=(ds18b20_queue,))
    ds18b20_thread.start()

    # Start FL808 reading thread
    fl808_thread = threading.Thread(target=fl808_sensor.read_fl808_thread, args=("/dev/gpiochip0", 5, fl808_queue))
    fl808_thread.start()

        # Initialize logging
    logger = logging.CSVLogger()

    
    start_time = time.time()

    while(True):
        try:
            time.sleep(0.1)
            print("\n--- MS4525 Readings ---")
            ms4525_data = ms4525_queue.get()
            print(conversions.convert_MS4525(ms4525_data[0][0], ms4525_data[0][1])) #purely for UI testing actual data is written to CSV
            
            print("\n--- SHT30 Readings ---")
            sht30_data = sht30_queue.get()
            print(conversions.convert_SHT30(sht30_data[0][0], sht30_data[0][1])) #purely for UI testing actual data is written to CSV
            print(conversions.convert_SHT30(sht30_data[1][0], sht30_data[1][1]))

            print("\n--- DS18B20 Readings ---")
            ds18b20_data = ds18b20_queue.get()
            print(ds18b20_data) 

            print("\n--- FL808 Readings ---")
            #fl808_data = fl808_queue.get()
            #print(f"Flow Rate: {fl808_data:.2f} L/min")

            # Log all data
            logger.save_data(ms4525_data, sht30_data, ds18b20_data)
            
        except KeyboardInterrupt:
            print("Exiting program.")
            break
        
        print(f"\nTotal execution time: {time.time() - start_time:.2f} seconds")


main()    







