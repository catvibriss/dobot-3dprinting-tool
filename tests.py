import serial
import time

# --- CONFIGURATION ---
PORT = "COM3"        # Change this to your port
BAUD = 115200        # Standard for 3D Firmware
SPEED_FAST = 2500    # Travel speed (mm/min)
SPEED_SLOW = 1000    # Printing/Corner speed

# --- COORDINATES ---
# NOTE: ТОЛЬКО ПРИ КАЛИБРКОЕ ПО БУМАЖКЕ!
X_MIN = -65
X_MAX = 50
Y_MIN = -85
Y_MAX = 90
Z_MAX = 110

# --- CONNECT ---
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"Connected to {PORT}. Waiting for reboot...")
    time.sleep(3)
except:
    print("Connection failed. Check Port and close Cura/Repetier.")
    exit()

def gsend(command, wait_time=0.1):
    cmd = command.strip() + "\r\n"
    ser.write(cmd.encode())
    time.sleep(wait_time)

    while ser.in_waiting:
        line = ser.readline().decode().strip()
        if line:
            print(f"[Bot]: {line}")

gsend("G1 X10 Y10 Z100")
gsend("M104 S0")
exit()
gsend("M105") # Get Temp
TEMP_TARGET = 200
# 2. Set Temperature
print(f">>> Setting Temp to {TEMP_TARGET}C...")
gsend(f"M104 S{TEMP_TARGET}") # M104 = Set Temp (No wait)

# 3. Wait loop (Monitor Temp)
print(">>> Warming up... (Press Ctrl+C to stop)")
while True:
    # Ask for current temperature
    # The robot will reply like: "ok T:25.4 /0.0 B:0.0 /0.0 @:0 B@:0"
    ser.write(b"M105\r\n")
    
    line = ser.readline().decode().strip()
    if "T:" in line:
        # Parse the messy string to get just the Temp number
        # "ok T:150.5 /200.0 ..."
        try:
            parts = line.split("T:")[1].split(" /")[0]
            temp = float(parts)
            print(f"Current Temp: {temp}°C")
            
            if temp >= TEMP_TARGET - 2:
                print(">>> Target Reached! Moving Robot...")
                break
                
        except:
            pass # Bad data packet
    
    time.sleep(1)

gsend("G1 E100 F200")

ser.close()