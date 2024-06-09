import serial

def setup_serial(port="COM5", baudrate=9600):
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = port
    ser.open()
    return ser

def send_move_to_arm(ser, move):
    start = move.getChessNotation()[:2]
    end = move.getChessNotation()[2:]
    command = f"{start}{end}\n"
    print(f"Sending command: {command}")  # Debugging line
    ser.write(command.encode())

def close_serial(ser):
    ser.close()
