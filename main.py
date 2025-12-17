import serial
import time

# --- CONFIGURATION ---
PORT = "COM3"        # Change this to your port
BAUD = 115200        # Standard for 3D Firmware
SPEED_FAST = 2500    # Travel speed (mm/min)
SPEED_SLOW = 1000    # Printing/Corner speed

# --- COORDINATES ---
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

def set_temperature(temp):
    gsend(f"M104 S{temp}")
    
def get_temperature():
    temp = 0
    
    ser.write(b"M105\r\n")
    
    line = ser.readline().decode().strip()
    if "T:" in line:
        parts = line.split("T:")[1].split(" /")[0]
        temp = float(parts)
    
    return temp

def range_map(x: float, x_min: float, x_max: float, out_min: float, out_max: float) -> float:
    return (x-x_min) * (out_max-out_min) / (x_max - x_min) + out_min

    