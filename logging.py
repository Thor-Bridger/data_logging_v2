import csv
import time
from datetime import datetime

class CSVLogger:
    def __init__(self):
        """
        When this class is started, it creates a new CSV file based on the
        current time and writes the specific headers.
        """
        # 1. Generate filename using current time (e.g., "2023-10-27_14-30-00.csv")
        self.filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        
        # 2. Open the file in write mode ('w')
        # newline='' is required for the csv module to handle line breaks correctly
        self.file = open(self.filename, mode='w', newline='')
        self.writer = csv.writer(self.file)

        # 3. Create the Header Row
        # This defines the columns in your Excel/CSV file
        headers = [
            "MS4525_Raw_P", 
            "MS4525_Raw_T", 
            "SHT30_1_Raw_T", 
            "SHT30_1_Raw_H", 
            "SHT30_2_Raw_T", 
            "SHT30_2_Raw_H",
            "DS18B20_Temps", # This will hold the list of temps
            "Timestamp"
        ]
        self.writer.writerow(headers)
        self.file.flush() # Ensure header is saved immediately
        print(f"Log file created: {self.filename}")

    def save_data(self, ms_data, sht_data, ds_data):
        """
        Takes raw data from sensors and writes one row to the CSV.
        """
        # Prepare an empty list for the row
        row = []

        # --- MS4525 Data ---
        # Structure: [[raw_p, raw_t]]
        # We want the first item in the list, then index 0 (pressure) and 1 (temp)
        if ms_data:
            row.append(ms_data[0][0])
            row.append(ms_data[0][1])
        else:
            row.extend(["None", "None"])

        # --- SHT30 Data ---
        # Structure: [[t1, h1], [t2, h2]]
        if sht_data and len(sht_data) >= 2:
            # Sensor 1
            row.append(sht_data[0][0])
            row.append(sht_data[0][1])
            # Sensor 2
            row.append(sht_data[1][0])
            row.append(sht_data[1][1])
        else:
            row.extend(["None", "None", "None", "None"])

        # --- DS18B20 Data ---
        # Structure: ([temp1, temp2...], [id1, id2...])
        # We only want the temperatures (index 0 of the tuple)
        if ds_data and len(ds_data) > 0:
            temps = ds_data[0] # This is the list of temperatures
            row.append(temps)  # Writes the whole list into one cell like "[24.5, 25.1]"
        else:
            row.append("None")

        # --- Timestamp ---
        row.append(time.time())

        # Write the row to the file
        self.writer.writerow(row)
        
        # Flush ensures data is physically written to the drive immediately
        # (Useful if power is cut or program crashes)
        self.file.flush()

    def close(self):
        self.file.close()