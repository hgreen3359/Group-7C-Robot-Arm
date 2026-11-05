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

    move.home_position(ser, LIMITS)
    trajectory = generate_trajectories.create_trajectory(25, 0, 0, current)

    
    # simulation.show_simulation(trajectory)
    current = move.send_trajectory(current, trajectory, ser, LIMITS)

    trajectory = generate_trajectories.create_trajectory(25, 0, 20, current)
    current = move.send_trajectory(current, trajectory, ser, LIMITS)


    

finally:
    ser.close()
