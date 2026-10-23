import time

# Channel numbers: check these against your arm's wiring
CH = {"base": 0, "shoulder": 1, "elbow": 2, "wrist_pitch": 3, "wrist_roll": 4, "gripper": 5}

def move_to(ser, limits, joint, pos, t=3000):
    lo, hi = limits[joint]
    pos = max(lo, min(hi, pos))          # clamp to the safe range
    ser.write(f"#{CH[joint]} P{pos} T{t}\r".encode())
    time.sleep(t / 1000)                 # wait for the move to finish

def gripper_activate(ser, limits, open_close):
    lo, hi = limits["gripper"]
    if open_close == "open":
        move_to(ser, limits, "gripper", hi)
    elif open_close == "close":
        move_to(ser, limits, "gripper", lo)


def home_position(ser, limits): # home position for the robot
    move_to(ser, limits, "base", 1500)
    move_to(ser, limits, "shoulder", 1500)
    move_to(ser, limits, "elbow", 1500)
    move_to(ser, limits, "wrist_pitch", 1500)
    move_to(ser, limits, "wrist_roll", 1500)
    gripper_activate(ser, limits, open_close="open")