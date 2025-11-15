import random
import time
from utils import *
from coordinate import Coordinate
from solution import Solution

def calculate_cluster_center(cluster_coordinates: list[Coordinate]) -> Coordinate:
    center_x = np.average([coordinate.get_x() for coordinate in cluster_coordinates])
    center_y = np.average([coordinate.get_y() for coordinate in cluster_coordinates])
    return Coordinate(center_x, center_y)

def assign_coordinate_to_cluster(coordinate: Coordinate, centers: list[Coordinate]) -> int:
    shortest_dist = float('inf')
    cluster_idx = -1
    for center_idx, center in enumerate(centers):
        distance_to_center = coordinate.distanceTo(center)
        if distance_to_center < shortest_dist:
            shortest_dist = distance_to_center
            cluster_idx = center_idx
    return cluster_idx
    

def k_means_clustering(k, coordinates: list[Coordinate]):
    clusters = {}
    old_clusters = None
    
    # Initialize Centers
    centers = random.sample(coordinates, k)
    
    while True:
        clusters = {i: [] for i in range(k)}
        
        # Decide class memberships
        for coordinate_idx, coordinate in enumerate(coordinates):
            assigned_cluster_idx = assign_coordinate_to_cluster(coordinate, centers)
            # Store indexes of each coordinate instead of the actual coordinate
            clusters[assigned_cluster_idx].append(coordinate_idx)
        
        # Calculate new centers
        for cluster_idx, cluster_coordinate_indexes in clusters.items():
            if len(cluster_coordinate_indexes) == 0:
                centers[cluster_idx] = random.choice(coordinates)
            else:
                # Retrive coordinates for a cluster using stored indexes
                cluster_coordinates = [coordinates[coordinate_idx] for coordinate_idx in cluster_coordinate_indexes]
                new_cluster_center = calculate_cluster_center(cluster_coordinates)
                # Update center for a cluster with the new center
                centers[cluster_idx] = new_cluster_center
        
        # Convergence check
        if clusters == old_clusters:
            break

        old_clusters = {k:v for k, v in clusters.items()}
    return centers, clusters

# Calculates the squared error for a cluster center and the actual coordinates assigned to it
def calculate_squared_error(center: Coordinate, coordinates: list[Coordinate]) -> float:
    return np.sum(np.square([center.distanceTo(coordinate) for coordinate in coordinates]))

# Calculates the sum of squared errors for all the cluster centers
def calculate_sum_squared_error(centers, clusters, coordinates):
    objective = 0
    for cluster_idx, cluster_coordinate_indexes in clusters.items():
        cluster_center = centers[cluster_idx]
        # Retrieve coordinates for a cluster using stored indexes
        cluster_coordinates = [coordinates[i] for i in cluster_coordinate_indexes]
        objective += calculate_squared_error(cluster_center, cluster_coordinates)
    return objective

def _find_nearest_neighbor(target: Coordinate, neighbors: list[int], coordinate_list: list[Coordinate], skip_chance):
    # NOTE: 'neighbors' is a list of indexes and needs to be converted into coordinate in coordinate_list
    # NOTE: 'skip_chance' is the probability that the nearest neighbor is skipped
    if len(neighbors) == 0:
        return None, float('inf')
    nearest_neighbor = neighbors[0]
    dist_bsf = target.distanceTo(coordinate_list[nearest_neighbor])
    for coord_idx in neighbors:
        dist = target.distanceTo(coordinate_list[coord_idx])
        # Update (or possibly skip) if distance is shorter than best so far
        if dist < dist_bsf and random.random() > skip_chance:
            dist_bsf = dist
            nearest_neighbor = coord_idx
    # Returns the index of the nearest_neighbor and the distance to it
    return nearest_neighbor, dist_bsf

def _find_route(start, coordinate_indexes, coordinate_list, chance):
    # Include distance from landing pad to first point in route
    first, distance = _find_nearest_neighbor(start, coordinate_indexes, coordinate_list, chance)
    route = [first]
    visited = set(route)
    while len(visited) < len(coordinate_indexes):
        # Only look for neighbors in at indexes that haven't been used yet
        unvisited_neighbors = [coordinate_index for coordinate_index in coordinate_indexes if coordinate_index not in visited]
        nn, nn_dist = _find_nearest_neighbor(coordinate_list[route[-1]], unvisited_neighbors, coordinate_list, chance)
        # No neighbors found
        if nn is None:
            break
        distance += nn_dist
        route.append(nn)
        visited.add(nn)
    # Add distance from last point in route to landing pad
    distance += start.distanceTo(coordinate_list[route[-1]])
    # Return the indexes of the coordinates in the route, and the total distance of the route
    return route, distance

def find_routes(centers, clusters, coordinates, duration, chance):
    results = []
    for cluster_idx, cluster_coords in clusters.items():
        start_time = time.time()
        route_bsf = None
        distance_bsf = float('inf')
        # search for better solutions w/ augmented nearest neighbor for 'duration' seconds
        while time.time() < start_time + duration:
            route, distance = _find_route(centers[cluster_idx], cluster_coords, coordinates, chance)
            # Keep the route with the shortest distance
            if distance < distance_bsf:
                distance_bsf = distance
                route_bsf = route
        results.append((route_bsf, distance_bsf))
    # Returns a list of tuples, where the first value is the route for the cluster and the second value is the total distance of the route
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
    max_drones = min(num_coordinates, 4)
    # Find routes for 1 to 4 drones
    for num_drones in range(1, max_drones+1):
        # Track best clusters
        centers_bsf = None
        clusters_bsf = None
        objective_function = float('inf')
        # Run multiple trials with random starts 
        for _ in range(100):
            centers, clusters = k_means_clustering(num_drones, coordinates)
            score = calculate_sum_squared_error(centers, clusters, coordinates)
            # Choose clusters with best (smallest) objective function
            if score < objective_function:
                objective_function = score
                centers_bsf = centers
                clusters_bsf = clusters
        # Route Finding
        # Duration is number of seconds to iterate, chance is probability of skipping best neighbor
        results = find_routes(centers_bsf, clusters_bsf, coordinates, duration=20, chance=0.10)
        
        # Set up inputs for Solution class
        servings_per_drone = [len(val) for val in clusters_bsf.values()]
        drone_routes = []
        drone_route_len = []
        for result in results:
            drone_routes.append(result[0])
            drone_route_len.append(result[1])
        total_route_len = sum(drone_route_len)
        
        # Create solution
        solution = Solution(num_drones, num_coordinates, total_route_len, centers_bsf, servings_per_drone, drone_route_len, drone_routes)
        solutions.append(solution)

        # Update command-line UI with progress
        print(solution)

    # Output Handling
    # TODO: Add visual route output
    solution_choice = int(input(f"Please select your choice 1 to {max_drones}: "))
    if solution_choice < 1 or solution_choice > max_drones:
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