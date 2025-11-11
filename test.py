from main import *

# TODO: Test center calculation in `calculate_cluster_center`
# TODO: Test SE calculation in `calculate_squared_error`
# TODO: Test SSE calculation in `calculate_sum_squared_error`

if __name__ == "__main__":
    centers = [Coordinate(5, 5), Coordinate(5, 10)]
    radius = 1
    num_points = 50
    all_x = []
    all_y = []
    coordinates_list = []
    for center in centers:
        x, y = generate_circle_points(center, radius, num_points)
        coordinates = [Coordinate(x1, y1) for x1, y1 in zip(x, y)]
        coordinates_list.append(coordinates)
        all_x.append(x)
        all_y.append(y)
    
    plot_circles(centers, all_x, all_y, radius)
