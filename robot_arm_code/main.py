import time

import init
import move
import generate_trajectories
import simulation
from coordinates import define_coordianates, coordinates_to_positions

ser = init.INIT()
initial_coords = init.inital_coords()



try:
    LIMITS = init.define_limits()
    current = [1500, 1500, 1500, 1500, 1500] 






    # #trajectory takes x,y,z
    # positions = [

    #     (18, 0, 10),
    #     # (20, 0, 10),
    #     # (20, 0, 10),


 
    # ]


    move.home_position(ser, LIMITS )

    coordinates = define_coordianates()
    positions = coordinates_to_positions(coordinates)

    for x, y, z, grip in positions:
        trajectory = generate_trajectories.create_trajectory(x, y, z, current)
        current = move.send_trajectory(current, trajectory, ser, LIMITS)   # move first
        move.gripper_activate(ser, LIMITS, open_close=grip)                # then set gripper
        time.sleep(0.5)







    # trajectory = generate_trajectories.create_trajectory(25, 0, 0, current)

    
    # # simulation.show_simulation(trajectory)
    # current = move.send_trajectory(current, trajectory, ser, LIMITS)

    # trajectory = generate_trajectories.create_trajectory(20, 0, 0, current)
    # current = move.send_trajectory(current, trajectory, ser, LIMITS)



finally:
    ser.close()
