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
    
def get_root_name(file_name: str) -> str:
    file_name_w_ext = os.path.basename(file_name)
    root_name = os.path.splitext(file_name_w_ext)[0]
    return root_name

# TODO: Create convert_solution_list() function which converts SOLUTION file to list of indexes 
# corresponding to order of points visited in SOLUTION.
# This will be utilized the same way as best_route in P1
# RETURNS list[int]
def convert_solution_list(file_name) -> list[int]:
    return [0, 0] # stub

# takes list of file_names and creates a unified "overall solution jpeg". Returns true if successful
def generate_overall_graph(file_names:list[str], input_name) -> bool:
    num_drones = len(file_names)
    
    drone_routes = []

    plot_color_dict = ["pink", "green", "blue", "yellow"]

    for index in num_drones:
        file_name = file_names[index]
        coordinates = parse_input(file_name)
        # TODO: Create convert_solution_list() function which converts SOLUTION file to list of indexes 
        # corresponding to order of points visited in SOLUTION.
        # This will be utilized the same way as best_route in P1
        
        solution_coordinates = convert_solution_list(file_name) # NOTE: needs above implementation

        x_coordinates, y_coordinates = get_plot_route(solution_coordinates)
        plot.plot(x_coordinates, y_coordinates, color=f"{plot_color_dict[index]}", marker=f"Drone #{index+1}",)
            
    plot.title(input_name[:-4] + " Visualization")
    plot.savefig(f"{input_name}_OVERALL_SOLUTION.jpeg")

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
    plot.xlabel("X")
    plot.ylabel("Y")
    plot.show()

def plot_clusters(clusters: list[int], coordinates: list[Coordinate]):
    if len(clusters) < 4: return
    colors = ["red", "green", "blue", "orange"]
    for idx in range(len(clusters)):
        x_coords = [coordinates[i].get_x() for i in clusters[idx]]
        y_coords = [coordinates[i].get_y() for i in clusters[idx]]
        plot.plot(x_coords, y_coords, color=colors[idx], marker="None")
    
    # 1950 x 1950 minimum
    dpi = 200
    min_w_pixels = 1920
    min_h_pixels = 1920
    figsize_w = min_w_pixels / dpi
    figsize_h = min_h_pixels / dpi

    # sets min dimensions as per instructions
    plot.figure(figsize=(figsize_w, figsize_h), dpi=dpi)

    # hide axes
    plot.subplot().set_axis_off()

    plot.show()
        
