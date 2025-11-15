# Team CyberSmiths K-Means Clustering Drone Pathfinder

A K-Means Clustering & Augmented Nearest Neighbors algorithm for optimal drone routes

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


<img width="313" height="49" alt="image" src="https://github.com/user-attachments/assets/3651bfd6-68b5-4880-9b94-5e0439187bdd" />

The program will begin searching for the best possible drone routes, when given one through four drones.
The estimated time to complete is five minutes.

The program will display four options, each correlated to the number of drones/routes. Each option presents unique route distances, landing pad coordinates, and servings per drone.
Choose one of the four options to continue:


<img width="680" height="304" alt="image" src="https://github.com/user-attachments/assets/f80a5632-8d07-4e2e-90c5-d3b0639aab09" />

The program will export the desired option to its own .txt solution files and .png visualization file.


<img width="1552" height="42" alt="image" src="https://github.com/user-attachments/assets/009727c4-7842-4461-a0f7-606597a01c8e" />

Example .png file:

<img width="665" height="627" alt="image" src="https://github.com/user-attachments/assets/cbbd3bf2-aa97-4c9b-8cb6-682d6f27c03a" />
