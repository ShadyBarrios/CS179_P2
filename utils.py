import matplotlib.pyplot as plot
import numpy as np
import os
from coordinate import Coordinate
from datetime import datetime

def valid_file(file_name: str) -> bool:
    # must be txt file
    if file_name[-4:] != ".txt":
        print("ERROR: File must be .txt type.")
        return False
    
    # must exist to be read
    if not os.path.isfile(file_name):
        print(f"ERROR: {file_name} not found")
        return False

    line_count = 0
    with open(file_name, "r") as file:
        data = file.read()
        line_count = data.count('\n')
    
    # check coordinate count
    if(line_count > 4096):
        print(f"ERROR: There must be at most 4096 nodes in {file_name}")
        return False
    elif(line_count == 0):
        print(f"ERROR: {file_name} is empty")
        return False
    
    return True

def parse_input(file_name: str) -> list[Coordinate]:
    coordinates:list[Coordinate] = []
    index = 0

    try:
        with open(file_name, "r") as file:
            while True:
                line = file.readline()
                index += 1

                # readline returns "" when EOF
                if line == "":
                    break

                coordinate_str = line.split()
                if len(coordinate_str) != 2:
                    print(f"ERROR: Improper coordinate formatting at line {index}")
                    exit()
                
                try:
                    x = float(coordinate_str[0])
                    y = float(coordinate_str[1])

                    # if x < 0 or y < 0:        # negative coordinates allowed per new information in Nov 9 email from Mr. Keogh
                    #     print(f"ERROR: Negative coordinates at line {index}")
                    #     exit()
                except ValueError:
                    print(f"ERROR: Improper coordinate at line {index}")
                    exit()

                coordinate = Coordinate(x,y)
                coordinates.append(coordinate)
    except FileNotFoundError:
        print(f"ERROR: {file_name} not found")
        exit()
    
    return coordinates

def parse_time(hour:int, minute:int):
    if hour < 0 or minute < 0:
        print("ERROR: Time components are negative...")
        exit()

    if minute >= 60:
        minute_rollover = (minute // 60)
        minute -= minute_rollover * 60
        hour += minute_rollover
    
    if hour >= 24:
        hour_rollover = (hour // 24)
        hour -= hour_rollover * 24
    
    if hour >= 12:
        meridiem = "pm"
    else:
        meridiem = "am"
    
    if hour == 0:
        hour = 12
    
    if hour > 12:
        hour -= 12
    
    time = f"{hour:02d}:{minute:02d}{meridiem}"
    return time

def get_end_time():
    dt = datetime.now()
    current_time = dt.time()
    hour, minute = (current_time.hour, current_time.minute)
    minute_predict = minute + 5 # only given five minutes to compute
    est_time = parse_time(hour, minute_predict)
    return est_time

def write_to_file(locations:list[int], file_name:str) -> bool:
    try:
        with open(file_name, "w") as file:
            for location in locations:
                line = f"{location+1}\n"
                file.write(line)
        return True
    except FileNotFoundError:
        print(f"ERROR: {file_name} could not be opened")
        return False
    
# takes list of file_names and creates a unified "overall solution jpeg". Returns true if successful
def generate_overall_graph(file_names:list[str]) -> bool:
    num_drones = len(file_names)
    
    file_line_counts = [] # stores number of lines per file (aka number of nodes given drone must visit)
    # output file is stored as a list of locations for drone to visit
    for file_name in file_names:
        line_count = 0
        with open(file_name, "r") as file:
            data = file.read()
            line_count = data.count('\n')
            x_coord, y_coord = get_plot_route()

            


        file_line_counts.append(line_count)

    # generate plot
    # plot.plot(x_coordinates, y_coordinates, color="pink", marker="o")
    # plot.plot(x_coordinates[0], y_coordinates[0], color="blue", marker="o")
    return False


def get_plot_route(route: list[int], coordinates: list[Coordinate]) -> tuple[list[int], list[int]]:
    # need to isolate the x and y coordinates for matplot
    x_coordinates = []
    y_coordinates = []
    for coord_idx in route:
        x_coordinates.append(coordinates[coord_idx-1].get_x())
        y_coordinates.append(coordinates[coord_idx-1].get_y())
    return tuple[x_coordinates, y_coordinates]


# Adapted from Dr. Keogh's Slides sent via email on 11/9/2025
def generate_circle_points(center: Coordinate, radius, num_points) -> tuple[list[float], list[float]]:
    
    x_center, y_center = center.get_x(), center.get_y()

    # Generate random angles
    angles = np.random.rand(num_points) * 2 * np.pi

    # Generate points from angles
    x_coordinates = radius * np.cos(angles) + x_center
    y_coordinates = radius * np.sin(angles) + y_center
    
    return x_coordinates, y_coordinates

def plot_circles(centers: list[Coordinate], x_coordinates: list[list[float]], y_coordinates: list[list[float]], radii: int):
    # Plot for confirmation + report figures
    plot.figure()
    for idx, center in enumerate(centers):
        x_center = center.get_x()
        y_center = center.get_y()
        circle_angles = np.linspace(0, 2*np.pi, 720)
        circle_x = radii * np.cos(circle_angles) + x_center
        circle_y = radii * np.sin(circle_angles) + y_center
        plot.plot(x_coordinates[idx], y_coordinates[idx], 'ro')
        plot.plot(circle_x, circle_y, 'b-')
    plot.axis('equal')
    plot.show()