import serial, time

def define_limits():
    LIMITS = {
        "base": (500, 2500),
        "shoulder": (1400, 1500),
        "elbow": (1600, 1700),
        "gripper": (900, 2100),
        "wrist": (2000, 2100),
    }
    return LIMITS

def INIT(port="COM5", baud=115200):
    ser = serial.Serial(port, baud, timeout=2)
    ser.dtr = True
    ser.rts = True
    time.sleep(1)

    ser.reset_input_buffer()
    ser.write(b"VER\r")
    time.sleep(1)
    print("VER:", ser.read(ser.in_waiting or 1))

    ser.write(b"Q\r")
    time.sleep(1)
    print("Q:", ser.read(ser.in_waiting or 1))

    return ser