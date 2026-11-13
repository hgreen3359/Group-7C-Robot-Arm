
def define_coordianates():
    coordinates = {(2,2), (3,3, (5,4))}

    return coordinates
def coordinates_to_positions(coordinates):
#8 by 4
    positions = []
    for x, y in coordinates:
        if 0 <= x <= 8 and 0 <= y <= 4:
            movement_x = coordinates[0] 
            movement_y = coordinates[1]
        else:
            print(f"Coordinate ({x}, {y}) is out of bounds.")