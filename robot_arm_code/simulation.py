"""sim_arm.py - generates a trajectory and plays it as an animation.
Needs: pip install matplotlib"""
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from init import L1, L2, L3, DT_MS
from trajectory import generate_trajectory, fk


# (x, y, z, pitch_deg, time_ms)
steps = [
    (20, 0, 15, 0, 1500),
    (25, 10, 6, -60, 2000),
    (25, 10, 3, -60, 1000),
    (22, 0, 18, -30, 2000),
    (25, -10, 6, -60, 2000),
    (25, -10, 3, -60, 1000),
    (50, 0, 10, 0, 1500),        # out of reach -> rejected
    (20, 0, 15, 0, 1500),
]
points = generate_trajectory(steps)

reach = L1 + L2 + L3
fig, (ax_side, ax_top) = plt.subplots(1, 2, figsize=(11, 5))
ax_side.set_xlim(-5, reach + 5); ax_side.set_ylim(-2, reach)
ax_side.set_aspect("equal"); ax_side.set_title("Side view")
ax_side.axhline(0, color="k", lw=1)
ax_top.set_xlim(-reach, reach); ax_top.set_ylim(-reach, reach)
ax_top.set_aspect("equal"); ax_top.set_title("Top view")
side, = ax_side.plot([], [], "o-", lw=4, color="tab:blue")
top, = ax_top.plot([], [], "o-", lw=4, color="tab:blue")
side_trail, = ax_side.plot([], [], lw=1, color="tab:red")
top_trail, = ax_top.plot([], [], lw=1, color="tab:red")
trail = []


def radial(x, y):
    return sqrt(x * x + y * y) * (1 if x >= 0 else -1)


def update(k):
    pts = fk(points[k])
    side.set_data([radial(x, y) for x, y, z in pts], [z for x, y, z in pts])
    top.set_data([x for x, y, z in pts], [y for x, y, z in pts])
    trail.append(pts[-1])
    side_trail.set_data([radial(x, y) for x, y, z in trail], [z for x, y, z in trail])
    top_trail.set_data([x for x, y, z in trail], [y for x, y, z in trail])


anim = FuncAnimation(fig, update, frames=len(points), interval=DT_MS, repeat=False)
plt.show()