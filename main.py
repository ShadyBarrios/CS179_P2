import random
import time
from utils import *
from coordinate import Coordinate
from solution import Solution

def k_means_clustering(k, coordinates: list[Coordinate]):
    clusters = {}
    old_clusters = None
    
    # Initialize Centers
    centers = random.sample(coordinates, k)
    
    while True:
        for i in range(k):
            clusters[i] = []
        
        # Decide class memberships
        for coordinate_idx, coordinate in enumerate(coordinates):
            shortest_dist = float('inf')
            cluster_idx = -1
            for center_idx, center in enumerate(centers):
                distance_to_center = coordinate.distanceTo(center)
                if distance_to_center < shortest_dist:
                    shortest_dist = distance_to_center
                    cluster_idx = center_idx
            clusters[cluster_idx].append(coordinate_idx)

        if clusters == old_clusters:
            break
        
        # Calculate new centers
        for cluster_idx, cluster_coords in clusters.items():
            x_sum = 0
            y_sum = 0
            for coordinate_idx in cluster_coords:
                x_sum += coordinates[coordinate_idx].get_x()
                y_sum += coordinates[coordinate_idx].get_y()
            if len(cluster_coords) == 0:
                print("ERROR: len(cluster_coords) == 0")
                continue
            centers[cluster_idx] = Coordinate(x_sum / len(cluster_coords), y_sum / len(cluster_coords))
        old_clusters = clusters
    return centers, clusters

def calculate_squared_error(centers, clusters, coordinate_list):
    objective = 0
    for cluster_idx, cluster_coords in clusters.items():
        cluster_center = centers[cluster_idx]
        for coordinate_idx in cluster_coords:
            objective += (cluster_center.distanceTo(coordinate_list[coordinate_idx])**2)
    return objective

def _find_nearest_neighbor(target: Coordinate, neighbors: list[int], visited: set[int], coordinate_list: list[Coordinate], chance):
    nearest_neighbor = None
    for coord_idx in neighbors:
        if coord_idx not in visited:
            nearest_neighbor = coord_idx
    dist_bsf = target.distanceTo(coordinate_list[nearest_neighbor])
    for coord_idx in neighbors:
        dist = target.distanceTo(coordinate_list[coord_idx])
        if dist < dist_bsf and coord_idx not in visited and random.random() > chance:
            dist_bsf = dist
            nearest_neighbor = coord_idx
    return nearest_neighbor, dist_bsf

def _find_route(start, coordinate_indexes, coordinate_list, chance):
    # Include distance from landing pad to first point in route
    first, distance = _find_nearest_neighbor(start, coordinate_indexes, set(), coordinate_list, 0)
    route = [first]
    visited = set(route)
    while len(visited) < len(coordinate_indexes):
        nn, nn_dist = _find_nearest_neighbor(coordinate_list[route[-1]], coordinate_indexes, visited, coordinate_list, chance)
        distance += nn_dist
        route.append(nn)
        visited.add(nn)
    # Add distance from last point in route to landing pad
    distance += start.distanceTo(coordinate_list[route[-1]])
    return route, distance

def find_routes(centers, clusters, coordinates, duration, chance):
    results = []
    for cluster_idx, cluster_coords in clusters.items():
        start_time = time.time()
        route_bsf = None
        distance_bsf = float('inf')
        while time.time() < start_time + duration:
            route, distance = _find_route(centers[cluster_idx], cluster_coords, coordinates, chance)
            if distance < distance_bsf:
                distance_bsf = distance
                route_bsf = route
        results.append((route_bsf, distance_bsf))
    return results

def main():
    # Input Handling
    input_file = input("Enter the name of the file: ")
    if not valid_file(input_file):
        exit()

    coordinates = parse_input(input_file)
    input_file_root = get_root_name(input_file)
    num_coordinates = len(coordinates)
    est_time = get_end_time()

    print(f"There are {num_coordinates} nodes: Solutions will be available in five minutes ({est_time})")

    solutions = []
    for num_drones in range(1, 5):
        # Run multiple trials with random starts 
        centers_bsf = None
        clusters_bsf = None
        objective_function = float('inf')
        for _ in range(100):
            centers, clusters = k_means_clustering(num_drones, coordinates)
            score = calculate_squared_error(centers, clusters, coordinates)
            if score < objective_function:
                objective_function = score
                centers_bsf = centers
                clusters_bsf = clusters
        # Route Finding
        results = find_routes(centers_bsf, clusters_bsf, coordinates, duration=20, chance=0.10)
        servings_per_drone = [len(val) for val in clusters_bsf.values()]
        drone_routes = []
        drone_route_len = []
        for result in results:
            drone_routes.append(result[0])
            drone_route_len.append(result[1])
        total_route_len = sum(drone_route_len)
        solution = Solution(num_drones, num_coordinates, total_route_len, centers_bsf, servings_per_drone, drone_route_len, drone_routes)
        solutions.append(solution)
        print(solution)

    # Output Handling
    # TODO: Add visual route output
    solution_choice = int(input("Please select your choice 1 to 4: "))
    if solution_choice < 1 or solution_choice > 4:
        print("Invalid choice")
        exit()
    chosen_solution:Solution = solutions[solution_choice-1]
    txt_export_successful, txt_file_names  = chosen_solution.export_to_txt_file("solutions", input_file_root)
    if txt_export_successful: # successful export
        output = "Writing "
        for file_name in txt_file_names:
            output += f"{file_name} "
        output += "to disk"
        print(output)
    else:
        print("Solution txt export unsuccessful")

    png_export_successful, png_file_name = chosen_solution.export_to_png_file("solutions", input_file_root, coordinates)
    if png_export_successful:
        print(f"Visualization successfully exported to {png_file_name}")
    else:
        print(f"Visualization export unsuccessful")


if __name__ == "__main__":
    main()