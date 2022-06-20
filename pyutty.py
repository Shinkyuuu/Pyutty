## IMPORTS ##
import serial
import serial.tools.list_ports
import sys
import os
import time

repeat = True

def getPorts():
    ports = serial.tools.list_ports.comports()
    found = dict()

    # Find and list all COM ports
    for i, p in enumerate(ports):
        found[i] = p.device
        print(f"{i}: {p.device}")
    
    # User chooses COM port
    if len(found) == 1: # If there is only 1, choose it
        print(f"Chose {found[0]}")
        return found[0]
    elif len(found) > 1: # User chooses port
        chosen = found[int(input("Chose COM Port (0, 1, ...): "))]
        print(f"Chose {chosen}")
        return chosen
    else: # There are no ports
        print("No COM Ports Open")
    
    return None

while repeat:
    port = getPorts()
    time.sleep(2)
    os.system("cls")

    if port:
        # Try to open serial port
        try:

            print(port)
            serialPort = serial.Serial(
                port = port,
                baudrate=115200,
                bytesize=8, 
                timeout=2, 
                stopbits=serial.STOPBITS_ONE
            )

        except:
            print("Unable to open serial port")
            
        else:
            # Read from the serial port
            while(1):
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
    
    # Ask if user wants to go again
    response = input("Would you like to open serial port again? (y/n): ")
    
    # If user says no, then end main loop
    if response.lower() != 'y':
        repeat = False
