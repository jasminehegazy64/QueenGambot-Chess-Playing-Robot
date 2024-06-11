import serial
import serial.tools.list_ports

def setup_serial():
    ports = serial.tools.list_ports.comports()
    serial_inst = serial.Serial()
    portlist = []

    for onePort in ports:
        portlist.append(str(onePort))
        print(str(onePort))

    serial_inst.baudrate = 9600
    serial_inst.port = "COM5"
    serial_inst.open()
    return serial_inst

def send_move_to_arm(ser, move):
    chess_notation = move.getChessNotation()

    # Check the length of the chess notation
    if len(chess_notation) == 5:
        # Skip the first character and send the rest
        start_pos = chess_notation[1:3]
        end_pos = chess_notation[3:]
    elif len(chess_notation) == 4:
        # Use the notation as it is
        start_pos = chess_notation[0:2]
        end_pos = chess_notation[2:]
    else:
        raise ValueError("Invalid chess notation length")

    move_command = start_pos + end_pos
    print(f"Sending command: {move_command}") 
    ser.write(move_command.encode())



def close_serial(ser):
    ser.close()
