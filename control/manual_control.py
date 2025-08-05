# control/manual_control.py

import serial
import time
from utils.config import SERIAL_PORT, BAUD_RATE

ser = None  # Global serial object

def connect_serial():
    """
    Initializes the serial connection to the robot.
    Returns a tuple: (success, message)
    """
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        return True, f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud"
    except serial.SerialException as e:
        return False, f"Serial Error: {str(e)}"

def is_connected():
    """Returns True if serial is open."""
    global ser
    return ser is not None and ser.is_open

def send_command(cmd):
    """
    Sends a single character command to the robot (w/a/s/d/x).
    """
    global ser
    if is_connected():
        try:
            ser.write(cmd.encode())
            return True, f"Sent command: {cmd.upper()}"
        except serial.SerialException as e:
            return False, f"Write Error: {str(e)}"
    else:
        return False, "Serial not connected."

def close_serial():
    """Closes the serial port safely."""
    global ser
    if is_connected():
        ser.close()
