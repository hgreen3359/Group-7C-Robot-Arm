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
from robot_arm_code import trajectory


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

#pca 9685 servo controller
def create_trajectory():
    step
return trajectory
