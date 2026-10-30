from time import time

import init
import move
import generate_trajectories
import simulation
ser = init.INIT()
initial_coords = init.inital_coords()




try:
    LIMITS = init.define_limits()
    current = move.home_position(ser, LIMITS)

    # current = move.move_to(ser, LIMITS, "base", 2000, current=current)
    # current = move.move_to(ser, LIMITS, "base", 1000, current=current)
    # current = move.move_to(ser, LIMITS, "base", 2000, current=current)
    # move.move_to(ser, LIMITS, "base", 1000, current=current)
    # move.gripper_activate(ser, LIMITS, open_close="close")
    trajectory = generate_trajectories.create_trajectory(10, 10, 10, current)
    simulation.show_simulation(trajectory)
finally:
    ser.close()
