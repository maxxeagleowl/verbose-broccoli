"""
HomeGuard Security System Simulator
Author: [Gunter Kleber]
Description: A smart home monitoring system that processes sensor readings
             and triggers alerts for security, safety, and comfort issues.
"""
 
import random
from datetime import datetime
 
# System configuration
HOME_MODES = ["HOME", "AWAY", "SLEEP"]
ALERT_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
 
# Current system state
current_mode = "AWAY"

#step 2
def create_sensor(sensor_id, location, sensor_type, threshold=None):
      
    sensor = {
        "sensor_id": sensor_id,
        "location": location,
        "sensor_type": sensor_type,
        "threshold": threshold
    }
    return sensor
 
def create_alert(severity, message, sensor_id, timestamp):
    
    alert = {
        "severity":severity,
        "message":message,
        "sensor_id":sensor_id,
        "timestamp":timestamp,
    }
    return alert
 
# Initialize sensors for the Peterson home
sensors = [
    create_sensor("1","living room","motion"), #motion for the living room 
    create_sensor(2,"kitchen", "temperature",60), #temperature for the kitchen with threshold
    create_sensor(3,"front door","door"), #door for the front door
    create_sensor(4,"bedroom","smoke")  #smoke for the bedroom 
]
# checkpoint step 2
print(f"Initialized {len(sensors)} sensors")
for sensor in sensors:
    print(f"  - {sensor['sensor_id']}: {sensor['location']} ({sensor['sensor_type']})")

# step 3

def is_abnormal_reading(sensor, reading_value):
    
    sensor_type = sensor["sensor_type"]

# Temp. Sensor
    if sensor_type == "temperature":
        if reading_value <35 or reading_value >95:
            return True
        else:
            return False
        
# Motion Sensor
    elif sensor_type == "motion":
        if reading_value == True:
            return True
        else:
            return False
        
# door sensor
    elif sensor_type == "door":
        if reading_value == "OPEN":
            return True
        else:
            return False

# smoke sensor
    elif sensor_type == "smoke":
        if reading_value == "DETECTED":
            return True
        else:
            return False
    
    else:
        return "unknown sensor"
    

#alert trigger

def should_trigger_security_alert(sensor,reading_value,system_mode):

    sensor_type = sensor["sensor_type"] #Sensor aus Datenbank holen

    if is_abnormal_reading(sensor,reading_value):
        if system_mode == "AWAY":
            return True
        elif system_mode == "HOME":
          return sensor["sensor_type"] == "smoke"
        elif system_mode == "SLEEP":
         return sensor["sensor_type"] in ["motion", "smoke"]
    return False

# Test temperature check
test_sensor = create_sensor("TEMP_TEST", "Test Room", "temperature", threshold=35)
print(f"34°F is abnormal: {is_abnormal_reading(test_sensor, 34)}")  # Should be True
print(f"68°F is abnormal: {is_abnormal_reading(test_sensor, 68)}")  # Should be False

# Test security alert
motion_sensor = create_sensor("MOTION_TEST", "Test Room", "motion")
print(f"Motion in AWAY mode triggers alert: {should_trigger_security_alert(motion_sensor, True, 'AWAY')}")  # Should be True
print(f"Motion in HOME mode triggers alert: {should_trigger_security_alert(motion_sensor, True, 'HOME')}")  # Should be False

# STEP4 Building Functions

# A realistic reading value based on sensor type

def generate_reading(sensor):

    sensor_type = sensor["sensor_type"]
    if sensor_type == "temperature":
        return random.randint(30, 100)
    elif sensor_type == "motion":
        return random.choice([True, False])
    elif sensor_type == "door":
        return random.choice(["OPEN", "CLOSED"])
    elif sensor_type == "smoke":
        return random.choice(["CLEAR", "DETECTED"])
    else:
        return None
 
# process definition reading sensors 
 
def process_reading(sensor, reading_value, system_mode):

    alerts = []
    timestamp = datetime.now().strftime("%H:%M:%S")

    sensor_name = sensor["sensor_id"]
    sensor_type = sensor["sensor_type"]
    location = sensor["location"]

    # Security alerts

    if system_mode == "AWAY":
        if sensor_type == "motion" and reading_value is True:
            alerts.append({
                "timestamp": timestamp,
                "severity": "HIGH",
                "message": f"Motion detected by {sensor_name} in {location} while system is AWAY."
            })

        if sensor_type == "door" and reading_value == "OPEN":
            alerts.append({
                "timestamp": timestamp,
                "severity": "HIGH",
                "message": f"Door opened at {location} while system is AWAY."
            })
    
    # Safety alerts
   
    if sensor_type == "motion" and reading_value is True:
        alerts.append({
        "timestamp": timestamp,
        "severity": "CRITICAL",
        "message": f"Motion detected by {sensor_name} in {location}!"
    })

    if sensor_type == "temperature":
        if reading_value <35:
            alerts.append({
                "timestamp": timestamp,
                "severity": "HIGH",
                "message": f"Low temperature detected in {location}: {reading_value}"
            })
        elif reading_value > 90:
            alerts.append({
                "timestamp": timestamp,
                "severity": "HIGH",
                "message": f"High temperature detected in {location}: {reading_value}"
            })

    # Comfort notifications (only in HOME mode)

    if system_mode == "HOME" and sensor_type == "temperature":
        if reading_value < 65 or reading_value > 75:
            alerts.append({
                "timestamp": timestamp,
                "severity": "LOW",
                "message": f"Temperature in {location} is {reading_value}°F"
            })

    return alerts 

# trigger alerts to show alert to user
 
def trigger_alert(alert):

    severity_symbol = {
        "LOW": "ℹ️",
        "MEDIUM": "⚠️",
        "HIGH": "🚨",
        "CRITICAL": "🔥"
    }
    
    symbol = severity_symbol.get(alert["severity"], "⚠️")
    print(f"[ALERT!] {symbol} {alert['severity']}: {alert['message']}")
 
def log_event(message, timestamp=None):
   
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[LOG] [{timestamp}] {message}")

# Test STEP 4

test_sensor = sensors[0]  # Motion sensor
reading = generate_reading(test_sensor)
print(f"Generated reading for {test_sensor['location']}: {reading}")
 
# Test processing
alerts = process_reading(test_sensor, True, "AWAY")
if alerts:
    trigger_alert(alerts[0])


# STEP 5


class Sensor:
        
    def __init__(self, sensor_id, location, sensor_type, threshold=None): #init - initialize the class #self - belongs to this class, only here
            self.sensor_id = sensor_id
            self.location = location
            self.sensor_type = sensor_type
            self.threshold = threshold
            self.current_value = None
         

    # A realistic reading value based on sensor type
    #      
    def read(self):
        if self.sensor_type == "temperature":
            self.current_value = random.randint(30,100)
        elif self.sensor_type == "motion":
            self.current_value = random.choice([True, False])
        elif self.sensor_type == "door":
            self.current_value = random.choice(["OPEN", "CLOSED"])
        elif self.sensor_type == "smoke":
            self.current_value = random.choice(["CLEAR", "DETECTED"])
        else:
            return None
            
        return self.current_value

            
    def isAbnormal(self):
        
        if self.current_value is None:
            return False
        if self.sensor_type == "temperature":
            return self.current_value < 35 or self.current_value > 95
        elif self.sensor_type == "motion":
            return self.current_value is True
        elif self.sensor_type == "door":
            return self.current_value == "OPEN"
        elif self.sensor_type == "smoke":
            return self.current_value == "DETECTED"
        else:
            return False

    
    def reset(self):     
        self.current_value = None
    
    def __str__(self):
        status = "No reading" if self.current_value is None else str(self.current_value)
        return f"{self.sensor_id} ({self.location}): {status}"

# Create sensor objects using the class

sensor_objects = [
    Sensor("MOTION_001", "Living Room", "motion"),
    Sensor("TEMP_001", "Kitchen", "temperature", 35),
    Sensor("DOOR_001", "Front Door", "door"),
    Sensor("SMOKE_001", "Bedroom", "smoke")
]

#test STEP 5

# Create and test a sensor
test_sensor = Sensor("TEST_001", "Test Room", "temperature", threshold=35)
test_sensor.read()
print(f"Sensor reading: {test_sensor.current_value}")
print(f"Is abnormal: {test_sensor.isAbnormal()}")
print(f"Sensor info: {test_sensor}")


# STEP 6

def run_simulation(duration_minutes=5, system_mode="AWAY"):
    """
    Runs the HomeGuard security system simulation.
    
    Parameters:
    - duration_minutes: How long to run the simulation
    - system_mode: HOME, AWAY, or SLEEP
    """
    print("=" * 50)
    print("=== HomeGuard Security System ===")
    print("=" * 50)
    print(f"Mode: {system_mode}\n")
    
    sensors = [
        Sensor("MOTION_001", "Living Room", "motion"),
        Sensor("TEMP_001", "Kitchen", "temperature", threshold=35),
        Sensor("DOOR_001", "Front Door", "door"),
        Sensor("SMOKE_001", "Bedroom", "smoke")
    ]
    
    import time

    for minute in range(duration_minutes):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\nTime: {current_time}")
        
        for sensor in sensors:
            reading = sensor.read()
            
            # Display reading
            if sensor.sensor_type == "temperature":
                status = "Normal" if 65 <= reading <= 75 else "Abnormal"
                print(f"[READING] {sensor.location} Temperature: {reading}°F ({status})")
            
            elif sensor.sensor_type == "motion":
                status = "DETECTED" if reading else "No activity"
                print(f"[READING] {sensor.location} Motion: {status}")
            
            elif sensor.sensor_type == "door":
                print(f"[READING] {sensor.location} Door: {reading}")
            
            elif sensor.sensor_type == "smoke":
                print(f"[READING] {sensor.location} Smoke: {reading}")
            
            # Convert object into dict for process_reading()
            sensor_dict = {
                "sensor_id": sensor.sensor_id,
                "location": sensor.location,
                "sensor_type": sensor.sensor_type,
                "threshold": sensor.threshold
            }
            
            alerts = process_reading(sensor_dict, reading, system_mode)
            
            for alert in alerts:
                trigger_alert(alert)
                if alert["severity"] in ["HIGH", "CRITICAL"]:
                    log_event("Sending notification to homeowner...")
        
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("Simulation complete!")
    print("=" * 50)

if __name__ == "__main__":
    run_simulation(duration_minutes=3, system_mode="AWAY")