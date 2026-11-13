
def define_coordianates():
    coordinates = {(4,2)}





    return coordinates

#11.5+5.75 = 17.25
def coordinates_to_positions(coordinates):
    positions = []
    for c in coordinates:
        if 1 <= c[0] <= 8 and 1 <= c[1] <= 4:
            positions.append((20 + (c[1] - 2) * 11.5, (4.5 - c[0]) * 11.5, 10, "open"))
            positions.append((20 + (c[1] - 2) * 11.5, (4.5 - c[0]) * 11.5, 5, "close"))
            positions.append((20 + (c[1] - 2) * 11.5, (4.5 - c[0]) * 11.5, 10,"close"))
            positions.append((20 + (1.5 - 2) * 11.5, (4.5 - 4) * 11.5, 10, "close"))
            positions.append((20 + (1.5 - 2) * 11.5, (4.5 - 4) * 11.5, 5, "open"))
            positions.append((20 + (1.5 - 2) * 11.5, (4.5 - 4) * 11.5, 10, "close"))

        else:
            print(f"Coordinate {c} is out of bounds.")
    return positions
