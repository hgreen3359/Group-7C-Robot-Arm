"""teach_sim.py - keyboard teach mode for the simulated arm.
Needs: pip install matplotlib

Click the plot window, then:
    1      next joint (base -> shoulder -> elbow -> wrist)
    w / s  increase / decrease the selected joint while held
           (angle change = DEG_PER_SEC x seconds held)
    Enter  build the trajectory from everything taught and play it
           (press Enter again to replay)
"""
import itertools
import json
import time
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Arm geometry, timing and limits come from your own init.py
from init import L1, L2, L3, DT_MS, HOME, LIMITS, US_PER_DEG
from trajectory import fk              # fk: pulses -> 3D points of each joint

DEG_PER_SEC = 30                       # teach speed
RATE = DEG_PER_SEC * US_PER_DEG        # pulses (us) per second held
MIN_HOLD_S = 0.05                      # ignore accidental taps
JOINTS = ["base", "shoulder", "elbow", "wrist"]   # position in this list = joint number

pose = list(HOME)                      # current taught pose (pulses)
joint = 0                              # selected joint index
waypoints = []                         # (target pose, time_ms) per key press
held = {}                              # key -> (time pressed, joint at press)


def clamp(j, v):
    # keep value v inside joint j's allowed pulse range from init.LIMITS
    return max(LIMITS[j][0], min(LIMITS[j][1], v))


def live_pose(now):
    """Taught pose plus any move still in progress (live preview)."""
    p = list(pose)                     # copy, so the real pose isn't changed by the preview
    for key, (t0, j) in held.items():  # look at every key currently held down
        if key in ("w", "s"):          # only w and s move a joint
            # distance moved so far = direction x speed x time held so far
            p[j] = clamp(j, pose[j] + (1 if key == "w" else -1) * RATE * (now - t0))
    return [round(v) for v in p]       # servo pulses are whole numbers


def key_down(key, t):
    global joint                       # needed because we assign to joint below
    if key in held:                    # ignore OS key auto-repeat
        return                         # (so hold time is measured from the first press)

    
    # choose the joint from the number key pressed
    # NOTE: the sim only has 4 joints (indices 0-3), so joint = 4 is out of range
    # and will cause an IndexError when the preview uses JOINTS[joint] / p[joint]
    match key: 
        case "0":
            joint = 0
        case "1":
            joint = 1
        case "2":
            joint = 2
        case "3":
            joint = 3
        case "4":
            joint = 4





    if key in ("0","1", "2", "3", "4", "w", "s"):
        held[key] = (t, joint)         # joint is locked at press time


def key_up(key, t):
    if key not in held:                # ignore releases we never saw the press for
        return
    t0, j = held.pop(key)              # when it was pressed, and which joint it was for
    # NOTE: "4" is in this tuple, so releasing the 4 key carries on past this line.
    # The code below treats any key that isn't "w" as a decrease, so it would
    # move joint j down. The tuple is probably meant to be just ("w", "s").
    if key not in ("w", "s", "4") or t - t0 < MIN_HOLD_S:
        return                         # not a move key, or a tap that was too short
    # new pulse = old pulse +/- (speed x time held), kept inside the limits
    new = round(clamp(j, pose[j] + (1 if key == "w" else -1) * RATE * (t - t0)))
    if new == pose[j]:
        return                         # already at the limit
    ms = abs(new - pose[j]) / RATE * 1000    # replay at the same speed as taught
    pose[j] = new                      # update the current taught pose
    waypoints.append((list(pose), ms)) # store a copy of the whole pose and how long the move takes
    print(f"{JOINTS[j]} -> {new} us ({ms:.0f} ms)")


def build_points():
    """Same format as generate_trajectory(): [base, shoulder, elbow, wrist] in us
    every DT_MS, with the same smooth start/stop."""
    points = [list(HOME)]              # trajectory always starts at the home pose
    for target, ms in waypoints:
        start = points[-1]             # each move starts where the previous one ended
        n = max(1, round(ms / DT_MS))  # number of DT_MS steps in this move (at least 1)
        for i in range(1, n + 1):
            t = i / n                  # progress through the move, 0 -> 1
            s = t * t * (3 - 2 * t)    # smoothstep: eases in and out instead of constant speed
            # blend every joint from its start value to its target by the eased progress s
            points.append([round(a + (b - a) * s) for a, b in zip(start, target)])
    return points


def main():
    plt.rcParams["keymap.save"] = []   # 's' and 'q' are matplotlib shortcuts
    plt.rcParams["keymap.quit"] = []   # clearing them stops them interfering with our keys

    # mode is "teach" (live preview) or "replay" (playing the trajectory)
    # k is the index of the trajectory point currently shown
    state = {"mode": "teach", "k": 0, "points": []}
    trail = []                         # gripper tip positions, drawn as the red path

    # ---- plot setup, same layout as sim_arm.py ----
    reach = L1 + L2 + L3               # maximum reach, used to size the axes
    fig, (ax_side, ax_top) = plt.subplots(1, 2, figsize=(11, 5))
    ax_side.set_xlim(-5, reach + 5); ax_side.set_ylim(-2, reach)
    ax_side.set_aspect("equal"); ax_side.set_title("Side view")
    ax_side.axhline(0, color="k", lw=1)                       # the table
    ax_top.set_xlim(-reach, reach); ax_top.set_ylim(-reach, reach)
    ax_top.set_aspect("equal"); ax_top.set_title("Top view")
    side, = ax_side.plot([], [], "o-", lw=4, color="tab:blue")        # arm, side view
    top, = ax_top.plot([], [], "o-", lw=4, color="tab:blue")          # arm, top view
    side_trail, = ax_side.plot([], [], lw=1, color="tab:red")         # tip path, side view
    top_trail, = ax_top.plot([], [], lw=1, color="tab:red")           # tip path, top view
    status = fig.suptitle("")          # text at the top showing mode and info

    def radial(x, y):
        # distance from the base in the arm's vertical plane (negative if x < 0);
        # used as the horizontal axis of the side view
        return sqrt(x * x + y * y) * (1 if x >= 0 else -1)

    def draw(pts):
        # pts is the list of joint positions from fk(); draw it in both views
        side.set_data([radial(x, y) for x, y, z in pts], [z for x, y, z in pts])
        top.set_data([x for x, y, z in pts], [y for x, y, z in pts])

    def on_press(event):
        if event.key == "enter":
            # save the taught waypoints so another script can load them later
            with open("taught_waypoints.json", "w") as f:
                json.dump(waypoints, f)
            # switch to replay mode, starting from the first trajectory point
            state.update(mode="replay", k=0, points=build_points())
            trail.clear()
        elif event.key:
            # monotonic() is a clock that never jumps backwards, good for timing holds
            key_down(event.key, time.monotonic())

    def on_release(event):
        if event.key:
            key_up(event.key, time.monotonic())

    def update(_):
        # runs every DT_MS milliseconds and draws one frame
        if state["mode"] == "teach":
            p = live_pose(time.monotonic())            # includes any move in progress
            draw(fk(p))
            status.set_text(f"TEACH  {JOINTS[joint]} = {p[joint]} us   "
                            f"waypoints: {len(waypoints)}   [Enter = play]")
            return
        # replay mode: show the next trajectory point each frame
        k, pts = state["k"], state["points"]
        if k < len(pts):
            frame = fk(pts[k])
            draw(frame)
            trail.append(frame[-1])                    # last fk point = gripper tip
            side_trail.set_data([radial(x, y) for x, y, z in trail], [z for x, y, z in trail])
            top_trail.set_data([x for x, y, z in trail], [y for x, y, z in trail])
            state["k"] += 1                            # move on to the next point next frame
            status.set_text(f"PLAYING {k + 1}/{len(pts)}")
        else:
            status.set_text("DONE   [Enter = replay]")

    # hook our handlers into matplotlib's keyboard events
    fig.canvas.mpl_connect("key_press_event", on_press)
    fig.canvas.mpl_connect("key_release_event", on_release)
    # call update() repeatedly (itertools.count never ends), once every DT_MS.
    # anim must stay assigned to a variable or Python deletes it and the animation stops
    anim = FuncAnimation(fig, update, frames=itertools.count(),
                         interval=DT_MS, cache_frame_data=False)
    plt.show()


if __name__ == "__main__":             # only run main() when this file is run directly
    main()