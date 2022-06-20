import serial

def readSerialLine(serialPort):
    try:
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):
            # Print the contents of the serial data
            return serialPort.readline().decode('Ascii')[:-1]
        else:
            return ''

    # If connection is lost or user types (ctrl + c)
    except:
        return None
    

def writeSerialLine(serialPort, message):
    serialPort.write((message + '\r').encode()) 