import time 
import serial 

def sendmovetoard(move ): #remember ya jasmika en el move lezme tebaa sent e5b4 keda 3shan el ard yefhamha 
    """
    hena simply kol el byhsal hwa en ana ba send values el moves lel arduino, el arduino ba hy- recieve el kalam dah we yefhamo bel 
    taree2a el ana hatargemha leh beha. which is the coordinates btaat el board, fa lama yakhod el dimensions btaat el baord
    ayan kan baa ezay dakhlnaha ehna manual aw through camera input, hy3raf en ,aslan 3 cms odam dah makan el pieace e7 maslan
    fa ayza el king yeroh mn elakh le elakh7, el masafa benhom 5 cm, pick up el piece (open and close gripper)
    move joint up, move other joint for 5 cm forward, joint dowwrds , gripper open

    """
    with serial.Serial('COM3', 9600, timeout=1) as ser:
        time.sleep(2) 
        ser.write(move.encode())

if __name__ == "__main__":
    move = "e2e4"  # Example move
    sendmovetoard(move)