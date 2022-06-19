## IMPORTS ##
import serial
import serial.tools.list_ports
from pick import pick
import sys
import os
import time

def getPorts():
    os.system("cls")
    ports = serial.tools.list_ports.comports()
    
    # User chooses COM port
    if len(ports) == 1: # If there is only 1, choose it
        print(f"Chose {ports[0]}")
        return ports[0]
    elif len(ports) > 1: # User chooses port
        title = 'Choose a COM Port: '
        port = pick(ports, title, indicator = '>')[0]
        print(f"Openning {port}")
        return port
    else: # There are no ports
        print("No COM Ports Open")
    
    return None

def readSerial():
    # Read from the serial port
    while(True):
        try:
            # Wait until there is data waiting in the serial buffer
            if(serialPort.in_waiting > 0):
                # Print the contents of the serial data
                print(serialPort.readline().decode('Ascii'), end = '')

        # If connection is lost or user types (ctrl + c)
        except:
            print("Connection Lost")
            serialPort.close()
            break
def start():
    repeat = True

    while repeat:
        port = getPorts()
        time.sleep(2)
        os.system("cls")

        if port:
            # Try to open serial port
            try:
                serialPort = serial.Serial(
                    port = COM7,
                    baudrate=115200,
                    bytesize=8, 
                    timeout=2, 
                    stopbits=serial.STOPBITS_ONE
                )
            except:
                print("Unable to open serial port")
                time.sleep(2)
            else:
                readSerial()
        
        # Ask if user wants to go again
        title = 'Try again?'
        choice = pick(['yes', 'no'], title, indicator = '>')[0]

        # If user says no, then end main loop
        repeat = True if choice == 'yes' else False
        
start()
        
os.system("cls")