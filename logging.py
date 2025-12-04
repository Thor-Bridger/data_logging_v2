import csv
import time
import os  
from datetime import datetime
from typing import Optional, List, Any, Tuple

# Define the expected types for clarity
DS18B20_Data = Optional[List[float]]
SHT30_Data = Optional[List[Tuple[float, float]]]
MS4525_Data = Optional[List[Tuple[float, float]]]
FL808_Data = Optional[float]


class CSVLogger:
    def __init__(self):
        """
        Creates a new CSV file inside the 'data_dump' folder.
        """
        folder = "data_dump"
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        self.full_path = os.path.join(folder, filename)
        
        self.file = open(self.full_path, mode='w', newline='')
        self.writer = csv.writer(self.file)

        # --- UPDATED HEADER ROW ---
        headers = [
            "MS4525_Raw_P", 
            "MS4525_Raw_T", 
            "SHT30_1_Raw_T", 
            "SHT30_1_Raw_H", 
            "SHT30_2_Raw_T", 
            "SHT30_2_Raw_H",
            "DS18B20_Temps",
            "FL808_Flow_Rate_LPM",  # <-- NEW HEADER FOR FL808
            "Timestamp"
        ]
        self.writer.writerow(headers)
        self.file.flush()
        
        print(f"Log file created at: {self.full_path}")

    # --- UPDATED save_data METHOD ---
    # Added fl_data parameter
    def save_data(self, ms_data: MS4525_Data, sht_data: SHT30_Data, ds_data: DS18B20_Data, fl_data: FL808_Data):
        """
        Takes raw data from sensors and writes one row to the CSV.
        """
        row: List[Any] = []

        # --- MS4525 Data ---
        if ms_data:
            row.append(ms_data[0][0])
            row.append(ms_data[0][1])
        else:
            row.extend(["None", "None"])

        # --- SHT30 Data ---
        if sht_data and len(sht_data) >= 2:
            row.append(sht_data[0][0])
            row.append(sht_data[0][1])
            row.append(sht_data[1][0])
            row.append(sht_data[1][1])
        else:
            row.extend(["None", "None", "None", "None"])

        # --- DS18B20 Data ---
        if ds_data and len(ds_data) > 0:
            # Note: Since DS18B20 can have multiple temps, we join them into a string
            row.append(str(ds_data)) 
        else:
            row.append("None")
        
        # --- FL808 Data (NEW LOGIC) ---
        if fl_data is not None:
            # The flow rate is a single float number
            row.append(f"{fl_data:.3f}") 
        else:
            row.append("None")

        # --- Timestamp ---
        row.append(time.time())

        self.writer.writerow(row)
        self.file.flush()

    def close(self):
        self.file.close()

# Note: You will need to update your main loop calls from:
# logger.save_data(ms4525_data, sht30_data, ds18b20_data) 
# to:
# logger.save_data(ms4525_data, sht30_data, ds18b20_data, None) # when fl808 data isn't ready
# and
# logger.save_data(ms4525_data, sht30_data, ds18b20_data, fl808_data) # when it is