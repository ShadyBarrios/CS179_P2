import math
# TODO: Input Handling

# TODO: Clustering Algorithm
class Coordinate:
    def __init__(self, x, y):
        self.loc = (round(x, 1), round(y, 1))
    
    # calculates the euclidean distance from self to arg coor
    def distanceTo(self, coor) -> float:
        x = self.loc[0] - coor.loc[0]
        y = self.loc[1] - coor.loc[1]
        x = x*x # will always be positive
        y = y*y # will always be positive
        dist = math.sqrt(x + y)
        return round(dist, 1)
    
    # determines if self is contained in arg of list[Coordinate]
    def isIn(self, coordinates: list) -> bool:
        for coordinate in coordinates:
            if coordinate.get_x() == self.get_x() and coordinate.get_y() == self.get_y():
                return True
        return False

    # returns formatted string for file writing
    def __str__(self) -> str:
        return f"{self.loc[0]}\t{self.loc[1]}"
    
    # getter for x coordinate
    def get_x(self) -> float:
        return self.loc[0]
    
    # getter for y coordinate
    def get_y(self) -> float:
        return self.loc[1]

# TODO: Route Finding

# TODO: Output Handling