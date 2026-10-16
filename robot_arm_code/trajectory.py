"""trajectory.py - kinematics and trajectory generation."""
from math import atan2, acos, sqrt, sin, cos, radians, degrees
from init import L0, L1, L2, L3, DT_MS, HOME, ZERO, SIGN, US_PER_DEG, LIMITS


def ik(x, y, z, pitch_deg):
    """Returns (base, shoulder, elbow, wrist) in radians, or None if out of reach."""
    pitch = radians(pitch_deg)
    base = atan2(y, x)
    r = sqrt(x * x + y * y)
    wr = r - L3 * cos(pitch)
    wz = (z - L0) - L3 * sin(pitch)
    c = (wr * wr + wz * wz - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    if abs(c) > 1:
        return None
    elbow = -acos(c)
    shoulder = atan2(wz, wr) - atan2(L2 * sin(elbow), L1 + L2 * cos(elbow))
    wrist = pitch - shoulder - elbow
    return base, shoulder, elbow, wrist


def angles_to_pulses(a):
    return [round(1500 + SIGN[i] * (degrees(a[i]) - ZERO[i]) * US_PER_DEG) for i in range(4)]


def pulses_to_angles(p):
    return [radians((p[i] - 1500) / (SIGN[i] * US_PER_DEG) + ZERO[i]) for i in range(4)]


def fk(p):
    """Pulses -> (x, y, z) of base, shoulder, elbow, wrist, tip."""
    base, s, e, w = pulses_to_angles(p)
    ex, ez = L1 * cos(s), L0 + L1 * sin(s)
    wx, wz = ex + L2 * cos(s + e), ez + L2 * sin(s + e)
    tx, tz = wx + L3 * cos(s + e + w), wz + L3 * sin(s + e + w)
    return [(r * cos(base), r * sin(base), z)
            for r, z in [(0, 0), (0, L0), (ex, ez), (wx, wz), (tx, tz)]]


def generate_trajectory(steps):
    """steps: list of (x, y, z, pitch_deg, time_ms).
    Returns a list of points [base, shoulder, elbow, wrist] in us, one every DT_MS."""
    points = [list(HOME)]
    for x, y, z, pitch, time_ms in steps:
        sol = ik(x, y, z, pitch)
        if sol is None:
            print(f"REJECTED: ({x}, {y}, {z}) is out of reach")
            continue
        target = [max(LIMITS[i][0], min(LIMITS[i][1], p))
                  for i, p in enumerate(angles_to_pulses(sol))]
        start = points[-1]
        n = max(1, time_ms // DT_MS)
        for i in range(1, n + 1):
            t = i / n
            s = t * t * (3 - 2 * t)          # smooth start and stop
            points.append([round(a + (b - a) * s) for a, b in zip(start, target)])
    return points