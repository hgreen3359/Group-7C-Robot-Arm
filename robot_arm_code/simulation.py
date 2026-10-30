
"""simulation.py - visualise an existing servo pulse trajectory."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from init import L0, L1, L2, L3, DT_MS, ZERO, SIGN, US_PER_DEG


def normalise_trajectory(trajectory):
    """Ensure the trajectory is a list of frames, each with 4 pulses."""

    if trajectory is None or len(trajectory) == 0:
        return []

    # Handle a single frame: [1500, 1500, 1500, 1500]
    if all(isinstance(value, (int, float)) for value in trajectory):
        if len(trajectory) == 4:
            return [list(trajectory)]

        raise ValueError(
            "A single frame must contain exactly 4 servo pulses. "
            f"Received: {trajectory}"
        )

    # Validate multiple frames.
    frames = []

    for i, frame in enumerate(trajectory):
        if not isinstance(frame, (list, tuple)):
            raise ValueError(
                f"Frame {i} is not a list of servo pulses: {frame!r}"
            )

        if len(frame) != 4:
            raise ValueError(
                f"Frame {i} must contain 4 servo pulses; "
                f"received {frame!r}"
            )

        frames.append(list(frame))

    return frames


def pulses_to_points(pulses):
    """Convert four servo pulses into approximate 3D joint positions."""

    angles = [
        (ZERO[i] + SIGN[i] * (pulses[i] - 1500) / US_PER_DEG)
        for i in range(4)
    ]

    from math import radians, sin, cos

    base, shoulder, elbow, wrist = [
        radians(angle) for angle in angles
    ]

    # Forward kinematics: calculate each link's position.
    a1 = shoulder
    a2 = shoulder + elbow
    a3 = shoulder + elbow + wrist

    r1 = L1 * cos(a1)
    z1 = L0 + L1 * sin(a1)

    r2 = r1 + L2 * cos(a2)
    z2 = z1 + L2 * sin(a2)

    r3 = r2 + L3 * cos(a3)
    z3 = z2 + L3 * sin(a3)

    # Rotate the arm around the base.
    points = [
        (0, 0, L0),
        (r1 * cos(base), r1 * sin(base), z1),
        (r2 * cos(base), r2 * sin(base), z2),
        (r3 * cos(base), r3 * sin(base), z3),
    ]

    return points


def show_simulation(trajectory):
    """Animate an existing trajectory. Does not generate new frames."""

    trajectory = normalise_trajectory(trajectory)

    if not trajectory:
        print("No trajectory provided.")
        return

    print(f"Simulating {len(trajectory)} frames.")

    reach = L1 + L2 + L3

    fig, (ax_side, ax_top) = plt.subplots(
        1, 2, figsize=(11, 5)
    )

    # Side view.
    ax_side.set_title("Robot Arm - Side View")
    ax_side.set_xlabel("Horizontal distance")
    ax_side.set_ylabel("Height")
    ax_side.set_xlim(-reach, reach)
    ax_side.set_ylim(-reach, reach)
    ax_side.set_aspect("equal")
    ax_side.axhline(0, color="black", linewidth=1)

    # Top view.
    ax_top.set_title("Robot Arm - Top View")
    ax_top.set_xlabel("X")
    ax_top.set_ylabel("Y")
    ax_top.set_xlim(-reach, reach)
    ax_top.set_ylim(-reach, reach)
    ax_top.set_aspect("equal")

    side_line, = ax_side.plot(
        [], [], "o-", linewidth=4, color="tab:blue"
    )
    top_line, = ax_top.plot(
        [], [], "o-", linewidth=4, color="tab:blue"
    )

    side_trail, = ax_side.plot(
        [], [], linewidth=1, color="tab:red"
    )
    top_trail, = ax_top.plot(
        [], [], linewidth=1, color="tab:red"
    )

    trail = []

    def update(i):
        # Use the existing servo pulse frame.
        pulses = trajectory[i]

        points = pulses_to_points(pulses)

        side_x = [
            (x * x + y * y) ** 0.5
            for x, y, z in points
        ]
        side_z = [z for x, y, z in points]

        top_x = [x for x, y, z in points]
        top_y = [y for x, y, z in points]

        side_line.set_data(side_x, side_z)
        top_line.set_data(top_x, top_y)

        trail.append(points[-1])

        side_trail.set_data(
            [(x * x + y * y) ** 0.5 for x, y, z in trail],
            [z for x, y, z in trail]
        )

        top_trail.set_data(
            [x for x, y, z in trail],
            [y for x, y, z in trail]
        )

        return side_line, top_line, side_trail, top_trail

    anim = FuncAnimation(
        fig,
        update,
        frames=len(trajectory),
        interval=DT_MS,
        repeat=False,
        blit=False
    )

    plt.tight_layout()
    plt.show()
