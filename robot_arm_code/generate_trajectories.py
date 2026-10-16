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


# ------------------------------------------------------------- KINEMATICS ---
def ik(x, y, z, pitch_deg):
    """Closed-form IK. Returns (base, shoulder, elbow, wrist) in radians, or None."""
    pitch = radians(pitch_deg)
    base = atan2(y, x)
    r = sqrt(x * x + y * y)
    wr = r - L3 * cos(pitch)                 # step back from tip to wrist joint
    wz = (z - L0) - L3 * sin(pitch)
    c = (wr * wr + wz * wz - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    if abs(c) > 1:
        return None                          # out of reach
    elbow = -acos(c)                         # elbow-up solution
    shoulder = atan2(wz, wr) - atan2(L2 * sin(elbow), L1 + L2 * cos(elbow))
    wrist = pitch - shoulder - elbow
    return base, shoulder, elbow, wrist


def angles_to_pulses(a):
    return [round(1500 + SIGN[ch] * (degrees(a[ch]) - ZERO[ch]) * US_PER_DEG)
            for ch in range(NUM_JOINTS)]


def pulses_to_angles(p):
    return [radians((p[ch] - 1500) / (SIGN[ch] * US_PER_DEG) + ZERO[ch])
            for ch in range(NUM_JOINTS)]


def fk(p):
    """Forward kinematics: pulses -> (x, y, z) of base, shoulder, elbow, wrist, tip."""
    base, s, e, w = pulses_to_angles(p)
    ex, ez = L1 * cos(s), L0 + L1 * sin(s)
    wx, wz = ex + L2 * cos(s + e), ez + L2 * sin(s + e)
    tx, tz = wx + L3 * cos(s + e + w), wz + L3 * sin(s + e + w)
    pts_rz = [(0, 0), (0, L0), (ex, ez), (wx, wz), (tx, tz)]
    return [(r * cos(base), r * sin(base), z) for r, z in pts_rz]


def clamp_pulses(p):
    """Pull every pulse back inside its joint limit."""
    return [max(LIMITS[ch][0], min(LIMITS[ch][1], int(p[ch]))) for ch in range(NUM_JOINTS)]


# ------------------------------------------------------------- TRAJECTORY ---
class Trajectory:
    def __init__(self, start=None):
        self.frames = [list(start or HOME)]

    def add_joint_move(self, pulses, time_ms=1500):
        """Ramp all joints (smoothstep) to the target pulses, arriving together."""
        target = clamp_pulses(pulses)            # safety: never leave the limits
        start = self.frames[-1]
        steps = max(1, time_ms // DT_MS)
        for i in range(1, steps + 1):
            t = i / steps
            s = t * t * (3 - 2 * t)              # slow start, slow end
            self.frames.append([round(a + (b - a) * s) for a, b in zip(start, target)])

    def add_move(self, x, y, z, pitch_deg, time_ms=1500):
        """Move the gripper tip to (x, y, z) cm. Returns False if out of reach."""
        sol = ik(x, y, z, pitch_deg)
        if sol is None:
            print(f"REJECTED: ({x}, {y}, {z}) pitch {pitch_deg} is out of reach")
            return False
        self.add_joint_move(angles_to_pulses(sol), time_ms)
        return True

    def save(self, path="trajectory.json"):
        with open(path, "w") as f:
            json.dump({"dt_ms": DT_MS, "frames": self.frames}, f)
        print(f"saved {len(self.frames)} points ({len(self.frames) * DT_MS / 1000:.1f} s) to {path}")


def load_trajectory(path="trajectory.json"):
    """Returns (frames, dt_ms)."""
    with open(path) as f:
        data = json.load(f)
    return data["frames"], data["dt_ms"]


def send_trajectory(ser, frames, dt_ms=DT_MS):
    """Play the points on the real SSC-32U (ser = an open pyserial port, e.g. from init.INIT()).
    Untested on hardware - try it slowly, with the arm clear of obstacles."""
    import time
    next_t = time.perf_counter()
    for frame in frames:
        safe = clamp_pulses(frame)               # clamp again before moving anything
        cmd = "".join(f"#{ch} P{p} " for ch, p in enumerate(safe))
        ser.write(f"{cmd}T{dt_ms}\r".encode())
        next_t += dt_ms / 1000
        time.sleep(max(0, next_t - time.perf_counter()))


if __name__ == "__main__":
    # Stand-in for the AI-generated procedure: (x, y, z, pitch_deg, time_ms)
    steps = [
        (20, 0, 15, 0, 1500),        # home
        (25, 10, 6, -60, 2000),      # above pick point
        (25, 10, 3, -60, 1000),      # pick
        (22, 0, 18, -30, 2000),      # lift
        (25, -10, 6, -60, 2000),     # above place point
        (25, -10, 3, -60, 1000),     # place
        (50, 0, 10, 0, 1500),        # deliberately unreachable -> rejected
        (20, 0, 15, 0, 1500),        # home
    ]
    traj = Trajectory()
    for x, y, z, pitch, t in steps:
        traj.add_move(x, y, z, pitch, t)
    traj.save("trajectory.json")