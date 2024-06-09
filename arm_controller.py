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
    start_pos = move.getChessNotation()[1:3]
    end_pos = move.getChessNotation()[3:]
    move_command = start_pos + end_pos
    print(f"Sending command: {move_command}") 
    ser.write(move_command.encode())


def close_serial(ser):
    ser.close()
