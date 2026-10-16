import time

# Channel numbers: check these against your arm's wiring
CH = {"base": 1, "shoulder": 2, "elbow": 3, "wrist": 4, "gripper": 5}

def move_to(ser, limits, joint, pos, t=3000):
    lo, hi = limits[joint]
    pos = max(lo, min(hi, pos))          # clamp to the safe range
    ser.write(f"#{CH[joint]} P{pos} T{t}\r".encode())
    time.sleep(t / 1000)                 # wait for the move to finish

def gripper_activate(ser, limits):
    lo, hi = limits["gripper"]
    move_to(ser, limits, "gripper", lo)
    move_to(ser, limits, "gripper", hi)