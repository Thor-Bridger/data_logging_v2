try:
    from w1thermsensor import W1ThermSensor
    _HAS_SENSOR = True
except Exception:
    # w1thermsensor not available on this system (e.g., running on desktop)
    W1ThermSensor = None
    _HAS_SENSOR = False
import time

def read_temperature():
    """Return a list of temperature readings from available sensors.

    If the `w1thermsensor` package or hardware is missing, return an
    empty list so callers can continue to operate (and logging will only
    record timestamps).
    """
    if not _HAS_SENSOR or W1ThermSensor is None:
        return []

    sensors = []
    ID = []
    try:
        for sensor in W1ThermSensor.get_available_sensors():
            temperature = sensor.get_temperature()
            ID.append(sensor.id)
            sensors.append(temperature)
        return sensors, ID
    except Exception:
        # map sensor-specific exceptions to an empty result for robustness
        return []
    
def one_wire_read_thread(ds18b20_queue):
    while True:
        try:
            temperatures, ids = read_temperature()
            ds18b20_queue.put((temperatures, ids))
        except KeyboardInterrupt:
            break
        except ValueError:
            time.sleep(0.1)
            continue