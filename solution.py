from coordinate import Coordinate
from utils import *
from os import makedirs as makedir
import matplotlib.pyplot as plot # pip install matplotlib

# encapsulates the "solutions"
class Solution:

    def __init__(self, num_drones:int, num_locations:int, total_route_len:float, landing_pads:list[Coordinate], servings_per_drone:list[int], drone_routes_len:list[float], drone_routes:list[list[int]]):
        if num_drones < 1 or num_drones > 4:
            print("ERROR: Invalid number of drones")
            exit()
        
        if total_route_len < 0:
            print("ERROR: Invalid route length")
            exit()
        
        if len(landing_pads) != num_drones:
            print("ERROR: Number of drones do not match number of landing pads")
            exit()
        
        if len(servings_per_drone) != num_drones or len(drone_routes_len) != num_drones:
            print(f"ERROR: Number of drone figures do not match number of drones")
            exit()
        
        if sum(servings_per_drone) != num_locations:
            print(f"ERROR: Drones serve more locations than there actually are")
            exit()
        
        if len(set(landing_pads)) != len(landing_pads):
            print(f"ERROR: There are duplicate landing pads")
            exit()

        all_route_points = sum(drone_routes, [])

        if len(set(all_route_points)) != len(all_route_points):
            print(f"ERROR: There are duplicate route points")
            exit()
        
        self.num_drones = num_drones
        self.num_locations = num_locations
        self.total_route_len = total_route_len
        self.landing_pads = landing_pads
        self.servings_per_drone = servings_per_drone
        self.drone_routes_len = drone_routes_len
        self.drone_routes = drone_routes
    
    def __str__(self) -> str:
        roman_nums = ["i", "ii", "iii", "iv"]
        output = f"\tIf you use {self.num_drones} drone(s), the total route will be {self.total_route_len:.1f} meters\n"

        for i in range(self.num_drones):
            output += f"\t{roman_nums[i]}.\tLanding Pad {i+1} "
            output += f"should be at [{int(self.landing_pads[i].get_x())},{int(self.landing_pads[i].get_y())}], "
            output += f"serving {self.servings_per_drone[i]} locations, "
            output += f"route is {self.drone_routes_len[i]:.1f} meters\n"
        
        return output

    def export_to_txt_file(self, directory:str, root_file_name:str) -> tuple[bool, list[str]]:
        makedir(directory, exist_ok=True) # create directory for exporting

        file_names:list[str] = []
        for i in range(self.num_drones):
            file_name = f"{directory}/{root_file_name}_{i+1}_SOLUTION_{int(self.drone_routes_len[i])}.txt"
            if write_to_file(self.drone_routes[i], file_name) == False: # failure
                return (False, [])
            file_names.append(file_name)
        
        return (True, file_names)
    
    def export_to_png_file(self, directory:str, root_file_name:str, coordinates:list[Coordinate]) -> tuple[bool, str]:
        route_colors = ["red", "green", "blue", "yellow"]
        landing_pad_colors = ["green", "red", "yellow", "blue"] # for contrast
        makedir(directory, exist_ok=True)

        file_name = root_file_name + "_OVERALL_SOLUTION.png"

        # 1950 x 1950 minimum
        dpi = 200
        min_w_pixels = 1950
        min_h_pixels = 1950
        figsize_w = min_w_pixels / dpi
        figsize_h = min_h_pixels / dpi

        # sets min dimensions as per instructions
        plot.figure(figsize=(figsize_w, figsize_h), dpi=dpi)

        # hide axes
        plot.subplot().set_axis_off()

        # 25% buffers around points
        plot.margins(x=0.25, y=0.25)
        
        for i in range(len(self.drone_routes)):
            x_coordinates = []
            y_coordinates = []
            for j in self.drone_routes[i]:
                x_coordinates.append(coordinates[j-1].get_x())
                y_coordinates.append(coordinates[j-1].get_y())
            plot.plot(x_coordinates, y_coordinates, color=route_colors[i], marker="None")
            plot.plot(self.landing_pads[i].get_x(), self.landing_pads[i].get_y(), color=landing_pad_colors[i], marker="o")
        plot.title(file_name[:-4] + " Visualization")
        file_name = directory + "/" + file_name
        try:
            plot.savefig(file_name)
        except FileNotFoundError:
            return (False, file_name)
        
        return (True, file_name)
