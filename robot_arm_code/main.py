from time import time

import init
import move

ser = init.INIT()





try:
    LIMITS = init.define_limits()
    move.home_position(ser, LIMITS)

    move.move_to(ser, LIMITS, "base", 2000)
    move.move_to(ser, LIMITS, "base", 1000)
    move.move_to(ser, LIMITS, "base", 2000)
    move.move_to(ser, LIMITS, "base", 1000)
    move.gripper_activate(ser, LIMITS, open_close="close")
finally:
    ser.close()