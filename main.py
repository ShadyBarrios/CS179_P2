import random
from datetime import datetime
from utils import *
from coordinate import Coordinate

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
            centers[cluster_idx] = Coordinate(x_sum / len(cluster_coords), y_sum / len(cluster_coords))
        old_clusters = clusters
    return centers, clusters

def calculate_squared_error(centers, clusters, coordinate_list):
    objective = 0
    for cluster_idx, cluster_coords in clusters.items():
        cluster_center = centers[cluster_idx]
        for coordinate_idx in cluster_coords:
            objective += (cluster_center.distanceTo(coordinate_list[coordinate_idx])**2)
    return round(objective, 2)

def _find_nearest_neighbor(target: Coordinate, neighbors: list[int], visited: set[int], coordinate_list: list[Coordinate]):
    nearest_neighbor = None
    dist_bsf = float('inf')
    for coord_idx in neighbors:
        dist = target.distanceTo(coordinate_list[coord_idx])
        if dist < dist_bsf and coord_idx not in visited:
            dist_bsf = dist
            nearest_neighbor = coord_idx
    return nearest_neighbor, dist_bsf

def _find_route(start, coordinate_indexes, coordinate_list):
    first, _ = _find_nearest_neighbor(start, coordinate_indexes, set(), coordinate_list)
    route = [first]
    visited = set(route)
    distance = 0
    while len(visited) < len(coordinate_indexes):
        nn, nn_dist = _find_nearest_neighbor(coordinate_list[route[-1]], coordinate_indexes, visited, coordinate_list)
        distance += nn_dist
        route.append(nn)
        visited.add(nn)
    return route, distance

def find_routes(centers, clusters, coordinates):
    results = []
    for cluster_idx, cluster_coords in clusters.items():
        route, distance = _find_route(centers[cluster_idx], cluster_coords, coordinates)
        results.append((route, distance))
    return results

def main():
    # TODO: Input Handling
    input_file = input("Enter the name of the file: ")
    input_file_root = input_file[:-4]
    if not valid_file(input_file):
        exit()

    coordinates = parse_input(input_file)
    # coordinates = [Coordinate(1, 1), Coordinate(1, 2), Coordinate(2, 1), Coordinate(6, 6), Coordinate(6, 5), Coordinate(5,6)]
    num_coordinates = len(coordinates)

    dt = datetime.now()
    current_time = dt.time()
    hour, minute = (current_time.hour, current_time.minute)
    minute_predict = minute + 5 # only given five minutes to compute
    est_time = parse_time(hour, minute_predict)

    print(f"There are {num_coordinates} nodes: Solutions will be available in five minutes ({est_time})")

    
    distance_matrix = [[coordinate_A.distanceTo(coordinate_B) for coordinate_B in coordinates] for coordinate_A in coordinates]
    # TODO: Cluster for all 1 <= k <= 4

    # Run multiple trials with random starts 
    centers_bsf = None
    clusters_bsf = None
    objective_function = float("inf")
    for _ in range(10):
        centers, clusters = k_means_clustering(2, coordinates)
        score = calculate_squared_error(centers, clusters, coordinates)
        if score < objective_function:
            objective_function = score
            centers_bsf = centers
            clusters_bsf = clusters
    print(objective_function)
    # TODO: Route Finding
    results = find_routes(centers, clusters, coordinates)
    print(results)

    # TODO: Output Handling
    # create your instances of Solution, each for the "m number of drones" solutions
    # then export using solution.export_to_file("solutions", input_file_root)
    # export_results  = solution.export_to_file("solutions", input_file_root)
    # export_successful = export_results[0]
    # file_names = export_results[1]
    # if export_results[0]: # successful export
    #     output = "Writing "
    #     for file_name in file_names:
    #         output += f"{file_name} "
    #     output += "to disk"
    #     print(output)
    # else:
    #     print("Solution export unsuccessful")


if __name__ == "__main__":
    main()