from main import *

def test_calculate_cluster_center(center, radius, num_points):
    x, y = generate_circle_points(center, radius, num_points)
    cluster_coordinates = [Coordinate(x1, y1) for x1, y1 in zip(x, y)]
    calculated_center = calculate_cluster_center(cluster_coordinates)
    print(f"Expected center: {center}")
    print(f"Calculated center: {calculated_center}")
    return calculated_center

def test_calculate_squared_error(center, radius, num_points, trials = 20):
    print(f"Expected OF Value: {(radius**2) * num_points}")
    total = 0
    for _ in range(trials):
        x, y = generate_circle_points(center, radius, num_points)
        cluster_coordinates = [Coordinate(x1, y1) for x1, y1 in zip(x, y)]
        total += calculate_squared_error(center, cluster_coordinates)
    print(f"Average OF over {trials} trials: {(total / trials):.3f}")

def test_cluster_assignment(centers, radius, num_points, colors):
    all_x = []
    all_y = []
    coordinate_list = []
    for center in centers:
        x, y = generate_circle_points(center, radius, num_points)
        all_x.append(x)
        all_y.append(y)
        cluster_coordinates = [Coordinate(x1, y1) for x1, y1 in zip(x, y)]
        coordinate_list.extend(cluster_coordinates)
    
    assigned_x = [[] for i in range(len(centers))]
    assigned_y = [[] for i in range(len(centers))]
    for coordinate in coordinate_list:
        idx = assign_coordinate_to_cluster(coordinate, centers)
        assigned_x[idx].append(coordinate.get_x())
        assigned_y[idx].append(coordinate.get_y())

    plot_circles(centers, all_x, all_y, radius)
    plot_circles(centers, assigned_x, assigned_y, radius, colors)


if __name__ == "__main__":
    print("===TESTING CENTER FINDING===")
    print("C: (0, 0), R: 1, N: 64")
    test_calculate_cluster_center(Coordinate(0, 0), 1, 64)
    print()
    print("C: (-5, -5), R: 1, N: 64")
    test_calculate_cluster_center(Coordinate(-5, -5), 1, 64)
    print()
    print("C: (5, 5), R: 1, N: 64")
    test_calculate_cluster_center(Coordinate(5, 5), 1, 64)
    print()

    print()
    print("===TESTING OBJECTIVE FUNCTION===")
    print("C: (0,0), R: 1, N: 64")
    test_calculate_squared_error(Coordinate(0, 0), 1, 64, trials=20)
    print()
    print("C: (0,0), R: 1, N: 128")
    test_calculate_squared_error(Coordinate(0, 0), 1, 128, trials=20)
    print()
    print("C: (0,0), R: 2, N: 64")
    test_calculate_squared_error(Coordinate(0, 0), 2, 64, trials=20)
    print()
    print("C: (0,0), R: 2, N: 128")
    test_calculate_squared_error(Coordinate(0, 0), 2, 128, trials=20)
    print()

    print("===TESTING CLUSTER ASSIGNMENT===")
    print("First image is dataset, second is cluster assignment")
    test_cluster_assignment([Coordinate(0, 0), Coordinate(5, 0)], 1, 64,  ["green", "orange"])
