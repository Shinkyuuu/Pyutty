## IMPORTS ##
import serial
import serial.tools.list_ports
import sys
import os
import time

## DEFINITIONS ##




# port = sys.argv[0]

# with serial.Serial() as ser:
#         ser.baudrate = 115200
#         ser.port = str(port)
#         ser.open()



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

port = getPorts()

time.sleep(2)
os.system("cls")

serialPort = serial.Serial(
    port = port,
    baudrate=115200,
    bytesize=8, 
    timeout=2, 
    stopbits=serial.STOPBITS_ONE
)

serialString = ""

try:
    while(1):
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            # Print the contents of the serial data
            print(serialString.decode('Ascii'), end = '')

except KeyboardInterrupt:
    serialPort.close()
    print("\nClosing Port")
    
    

serialPort.close()