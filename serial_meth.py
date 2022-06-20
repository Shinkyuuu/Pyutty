import serial

def readSerialLine():
    try:
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Print the contents of the serial data
            return str(serialPort.readline().decode('Ascii'), end = '')
    # If connection is lost or user types (ctrl + c)
    except:
        serialPort.close()
        return None

def writeSerialLine():
    pass