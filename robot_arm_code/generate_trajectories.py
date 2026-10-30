"""
trajectory.py - all the calculations: kinematics + trajectory generation.

A trajectory is a list of frames. Each frame is 4 pulses (us), one per channel,
and consecutive frames are DT_MS (20 ms) apart. The SAME points are used to
  * drive the real arm   -> send_trajectory(ser, frames)
  * simulate the arm     -> python sim_arm.py trajectory.json

Arm parameters (link lengths, limits, calibration) come from init.py.
Run:  python trajectory.py      (writes trajectory.json)
"""
import json
from math import atan2, acos, sqrt, sin, cos, radians, degrees
from init import L0, L1, L2, L3, NUM_JOINTS, DT_MS, HOME, ZERO, SIGN, US_PER_DEG, LIMITS

import numpy as np
from move import current








# ------------------------------------------------------------- KINEMATICS ---
def ik(x, y, z, pitch_deg):
    pitch = radians(pitch_deg)
    r = sqrt (x * x + y * y)
    wr = r - L3 * cos(pitch)    
    wz = (z - L0) - L3 * sin(pitch)
    c = (wr * wr + wz * wz - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    if abs(c) > 1:
        return None
    elbow = -acos(c)
    shoulder = atan2(wz, wr) - atan2(L2 * sin(elbow), L1 + L2 * cos(elbow))
    wrist = pitch - shoulder - elbow
    joint_angles = [atan2(y, x), shoulder, elbow, wrist]
    return joint_angles


def angles_to_pulses(joint_angles):
    pulses = []
    for i in range(len(joint_angles)):
        pulse = round(1500 + SIGN[i] * (degrees(joint_angles[i]) - ZERO[i]) * US_PER_DEG)
        pulses.append(pulse)
    return pulses


def angular_distance(pulses, current):

    distance = sqrt((pulses[0]- current[0])**2+(pulses[1]- current[1])**2 + (pulses[2]- current[2])**2+(pulses[3]- current[3])**2)
    print("angular distance", distance)

    return distance


#pca 9685 servo controller
def create_trajectory(x,y,z, joint_angles):
    joint_angles = ik(x, y, z, 0)
    pulses = angles_to_pulses(joint_angles)
    distance = angular_distance(pulses, current)
    time_steps = max(1, int(distance / 10))

    
    trajectory = []
    for i in range(time_steps):
        frame = []
        for j in range(len(joint_angles)):
            frame.append(int(
                current[j] + (pulses[j] - current[j]) * (i + 1) / time_steps
            ))
        trajectory.append(frame) 

    print("trajectory", trajectory)
    return trajectory

"""
trajectory.py - all the calculations: kinematics + trajectory generation.

A trajectory is a list of frames. Each frame is 4 pulses (us), one per channel,
and consecutive frames are DT_MS (20 ms) apart. The SAME points are used to
  * drive the real arm   -> send_trajectory(ser, frames)
  * simulate the arm     -> python sim_arm.py trajectory.json

Arm parameters (link lengths, limits, calibration) come from init.py.
Run:  python trajectory.py      (writes trajectory.json)
"""
import json
from math import atan2, acos, sqrt, sin, cos, radians, degrees
from init import L0, L1, L2, L3, NUM_JOINTS, DT_MS, HOME, ZERO, SIGN, US_PER_DEG, LIMITS

import numpy as np
from move import current








# ------------------------------------------------------------- KINEMATICS ---
def ik(x, y, z, pitch_deg):
    pitch = radians(pitch_deg)
    r = sqrt (x * x + y * y)
    wr = r - L3 * cos(pitch)    
    wz = (z - L0) - L3 * sin(pitch)
    c = (wr * wr + wz * wz - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    if abs(c) > 1:
        return None
    elbow = -acos(c)
    shoulder = atan2(wz, wr) - atan2(L2 * sin(elbow), L1 + L2 * cos(elbow))
    wrist = pitch - shoulder - elbow
    joint_angles = [atan2(y, x), shoulder, elbow, wrist]
    return joint_angles


def angles_to_pulses(joint_angles):
    pulses = []
    for i in range(len(joint_angles)):
        pulse = round(1500 + SIGN[i] * (degrees(joint_angles[i]) - ZERO[i]) * US_PER_DEG)
        pulses.append(pulse)
    return pulses


def angular_distance(pulses, current):

    distance = sqrt((pulses[0]- current[0])**2+(pulses[1]- current[1])**2 + (pulses[2]- current[2])**2+(pulses[3]- current[3])**2)
    print("angular distance", distance)

    return distance


#pca 9685 servo controller
def create_trajectory(x,y,z, joint_angles):
    joint_angles = ik(x, y, z, 0)
    pulses = angles_to_pulses(joint_angles)
    distance = angular_distance(pulses, current)
    time_steps = max(1, int(distance / 10))

    
    trajectory = []
    for i in range(time_steps):
        frame = []
        for j in range(len(joint_angles)):
            frame.append(int(
                current[j] + (pulses[j] - current[j]) * (i + 1) / time_steps
            ))
        trajectory.append(frame) 

    print("trajectory", trajectory)
    return trajectory

