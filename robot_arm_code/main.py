import time

import init
import move
import generate_trajectories
import simulation
ser = init.INIT()
initial_coords = init.inital_coords()



try:
    LIMITS = init.define_limits()
    current = [1500, 1500, 1500, 1500, 1500] 






    #trajectory takes x,y,z
    positions = [

        (18, 0, 0),
        (18, 0, 10),
        (18, 10, 0),
        (18, -10, 5),
        (23, 0, 0)

 
    ]

    move.home_position(ser, LIMITS )

    for x, y, z in positions:
        trajectory = generate_trajectories.create_trajectory(x, y, z, current)
        current = move.send_trajectory(current, trajectory, ser, LIMITS)





    # trajectory = generate_trajectories.create_trajectory(25, 0, 0, current)

    
    # # simulation.show_simulation(trajectory)
    # current = move.send_trajectory(current, trajectory, ser, LIMITS)

    # trajectory = generate_trajectories.create_trajectory(20, 0, 0, current)
    # current = move.send_trajectory(current, trajectory, ser, LIMITS)



finally:
    ser.close()
