import init
import move

ser = init.INIT()
try:
    LIMITS = init.define_limits()

    move.move_to(ser, LIMITS, "base", 1500)
    move.move_to(ser, LIMITS, "shoulder", 1500)
    move.move_to(ser, LIMITS, "elbow", 1500)
    move.move_to(ser, LIMITS, "wrist", 1500)
    move.gripper_activate(ser, LIMITS)
finally:
    ser.close()