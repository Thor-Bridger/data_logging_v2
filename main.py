import i2c_sensors
import DS18B20_sensor
import fl808_sensor
import conversions
import logging

import time
import queue
import threading
from queue import Empty # <-- Import the specific exception

# (Assume your CSVLogger class and thread targets are defined elsewhere)

def main():
    # Create queues for inter-thread communication
    ds18b20_queue = queue.Queue()
    sht30_queue = queue.Queue()
    ms4525_queue = queue.Queue()
    fl808_queue = queue.Queue()

    # Start threads (assuming this part is correct)
    i2c_read_thread = threading.Thread(target=i2c_sensors.i2c_read_thread, args=(sht30_queue, ms4525_queue))
    ds18b20_thread = threading.Thread(target=DS18B20_sensor.one_wire_read_thread, args=(ds18b20_queue,))
    fl808_thread = threading.Thread(target=fl808_sensor.read_fl808_thread, args=("/dev/gpiochip0", 5, fl808_queue))
    
    i2c_read_thread.start()
    ds18b20_thread.start()
    fl808_thread.start()

    # Initialize logging
    logger = logging.CSVLogger()
    
    start_time = time.time()

    while(True):
        # 1. Loop runs continuously without blocking
        time.sleep(0.1) # Small loop delay to prevent 100% CPU usage
        
        # --- MS4525 Readings ---
        try:
            ms4525_data = ms4525_queue.get(block=False) # NON-BLOCKING READ
            print("\n--- MS4525 Readings ---")
            print(conversions.convert_MS4525(ms4525_data[0][0], ms4525_data[0][1]))
            logger.save_data(ms4525_data, None, None, None) # Log immediately after processing
        except Empty:
            pass # Ignore the error and continue the loop

        # --- SHT30 Readings ---
        try:
            sht30_data = sht30_queue.get(block=False) # NON-BLOCKING READ
            print("\n--- SHT30 Readings ---")
            print(conversions.convert_SHT30(sht30_data[0][0], sht30_data[0][1]))
            print(conversions.convert_SHT30(sht30_data[1][0], sht30_data[1][1]))
            logger.save_data(None, sht30_data, None, None) # Log immediately after processing
        except Empty:
            pass # Ignore the error and continue the loop

        # --- DS18B20 Readings ---
        try:
            ds18b20_data = ds18b20_queue.get(block=False) # NON-BLOCKING READ
            print("\n--- DS18B20 Readings ---")
            print(ds18b20_data) 
            logger.save_data(None, None, ds18b20_data, None) # Log immediately after processing
        except Empty:
            pass # Ignore the error and continue the loop

        # --- FL808 Readings ---
        try:
            fl808_data = fl808_queue.get(block=False) # NON-BLOCKING READ
            print("\n--- FL808 Readings ---")
            print(f"Flow Rate: {fl808_data:.2f} L/min")
            # Log flow rate (assuming logger can handle it)
            logger.save_data(None, None, None, fl808_data) 
        except Empty:
            pass # Ignore the error and continue the loop
        
        # Print execution time after checking all queues
        print(f"\nTotal execution time: {time.time() - start_time:.2f} seconds")

# Call main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program shut down.")
        # NOTE: You would need to add code here to stop your threads cleanly (e.g., setting a global STOP_FLAG)