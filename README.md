# Team CyberSmiths K-Means Clustering Drone Pathfinder

A K-means Clustering & Augmented Nearest Neighbors algorithm for optimal drone routes

## Installation

> [!IMPORTANT]
> Python 3 must be installed. You can install it [here](https://www.python.org/downloads/)

Clone the repository using git:

```bash
git clone https://github.com/ShadyBarrios/CS179_P2.git
```

Navigate to the project folder:

```bash
cd CS179_P2
```

Install the required dependencies with pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the program using python:

```bash
python main.py
```

Enter the path to the location text file when prompted:

The program will begin searching for the best possible drone routes, when given one through four drones.
The estimated time to complete is five minutes.

The program will display four options, each correlated to the number of drones/routes. Each option presents unique route distances, landing pad coordinates, and servings per drone.

Choose one of the four options to continue:

The program will export the desired option to its own .txt solution file and .png visualization file.