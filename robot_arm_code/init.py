import serial, time





# ------------------------------------------------------- ARM PARAMETERS ---
# Lynxmotion AL5D datasheet: shoulder-elbow 5.75", elbow-wrist 7.375",
# wrist-gripper tip 3.375". L0 is derived from the 19.00" "reaching up" height.
# Measure L0 on your arm, and update L1-L3 once your extension is fitted.
L0 = 6.35    # cm, table to shoulder joint height (derived, approx)
L1 = 14.61   # cm, shoulder -> elbow
L2 = 18.73   # cm, elbow -> wrist
L3 = 8.57    # cm, wrist -> gripper tip
 
NUM_JOINTS = 5                      # channel: 0 base, 1 shoulder, 2 elbow, 3 wrist, 4 gripper
DT_MS = 20                          # one trajectory point per 20 ms servo period
HOME = [1500, 1500, 1500, 1500, 1500]     # pulses (us) at start-up
 
# Geometric angle conventions used by the IK in trajectory.py:
#   base      : 0 = pointing along +x
#   shoulder  : angle of link 1 above horizontal (90 = straight up)
#   elbow     : angle of link 2 relative to link 1 (negative = elbow-up bend)
#   wrist     : angle of link 3 relative to link 2
#   gripper   : angle of link 4 relative to link 3
ZERO = [0, 90, -90, 0, 0]              # geometric angle (deg) at a 1500 us pulse
SIGN = [1, 1, 1, 1, 1]                 # flip to -1 if a servo is mounted reversed
US_PER_DEG = 10.0                   # calibrate against your servos
LIMITS = [(700, 2300)] * NUM_JOINTS # pulse limits (us) per channel - set the real safe ranges
 







def define_limits():
    LIMITS = {
        "base": (500, 2500),
        "shoulder": (1400, 1500),
        "elbow": (1600, 1700),
        "gripper": (900, 2100),
        "wrist_pitch": (1000, 2100),
        "wrist_roll": (1000, 2000),
    }
    return LIMITS




def INIT(port="COM6", baud=115200):
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

