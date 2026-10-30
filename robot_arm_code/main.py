from time import time

import init
import move
import generate_trajectories
import simulation
ser = init.INIT()
initial_coords = init.inital_coords()
<<<<<<< HEAD

=======
>>>>>>> 92b3339020624da1e95ffbbed7c0ade66c4cd0a2




try:
    LIMITS = init.define_limits()
<<<<<<< HEAD
    # current = move.home_position(ser, LIMITS)
    current = [1500, 1500, 1500, 1500, 1500] 
    # current = move.move_to(ser, LIMITS, "base", 2000, current=current)
    # current = move.move_to(ser, LIMITS, "base", 1000, current=current)
    # current = move.move_to(ser, LIMITS, "base", 2000, current=current)
    # move.move_to(ser, LIMITS, "base", 1000, current=current)
    # move.gripper_activate(ser, LIMITS, open_close="close")


    trajectory = generate_trajectories.create_trajectory(20, 0, -5, current)
    # simulation.show_simulation(trajectory)

    for frame in trajectory:

        current = move.move_to(ser, LIMITS, "base", frame[0], current=current)
        current = move.move_to(ser, LIMITS, "shoulder", frame[1], current=current)
        current = move.move_to(ser, LIMITS, "elbow", frame[2], current=current)
        current = move.move_to(ser, LIMITS, "wrist_pitch", frame[3], current=current)
        

    # trajectory = generate_trajectories.create_trajectory(12, 0, 15, current)
    
    # for frame in trajectory:

    #     current = move.move_to(ser, LIMITS, "base", frame[0], current=current)
    #     current = move.move_to(ser, LIMITS, "shoulder", frame[1], current=current)
    #     current = move.move_to(ser, LIMITS, "elbow", frame[2], current=current)
    #     current = move.move_to(ser, LIMITS, "wrist_pitch", frame[3], current=current)
        
=======
    current = move.home_position(ser, LIMITS)

    # current = move.move_to(ser, LIMITS, "base", 2000, current=current)
    # current = move.move_to(ser, LIMITS, "base", 1000, current=current)
    # current = move.move_to(ser, LIMITS, "base", 2000, current=current)
    # move.move_to(ser, LIMITS, "base", 1000, current=current)
    # move.gripper_activate(ser, LIMITS, open_close="close")
    trajectory = generate_trajectories.create_trajectory(10, 10, 10, current)
    simulation.show_simulation(trajectory)
>>>>>>> 92b3339020624da1e95ffbbed7c0ade66c4cd0a2
finally:
    ser.close()
