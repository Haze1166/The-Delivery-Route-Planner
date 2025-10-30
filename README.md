# The Ultimate Delivery Route Planner

This project is a command-line application that simulates a daily workflow for a delivery logistics company. It uses three core algorithms to optimize operations:

1.  **0/1 Knapsack Algorithm**: To select the most valuable set of packages to load onto a truck without exceeding its weight capacity.
2.  **Hamiltonian Cycle Algorithm**: To find an efficient round-trip route that visits all delivery locations exactly once.
3.  **Linear Search Algorithm**: To allow the driver to quickly look up details for a specific package on their manifest.

## Project Structure

-   `main.py`: The main script that orchestrates the entire workflow.
-   `algorithms/`: A module containing the implementations of the core algorithms.
    -   `knapsack.py`: Implements the 0/1 Knapsack algorithm using dynamic programming.
    -   `hamiltonian.py`: Implements a backtracking algorithm to find a Hamiltonian Cycle.
    -   `linear_search.py`: Implements a simple linear search.
-   `data/`: Contains the sample data for the simulation.
    -   `packages.csv`: A list of all available packages in the warehouse.
    -   `locations.csv`: A distance matrix for all possible locations.

## How to Run

1.  Ensure you have Python 3 installed.
2.  Place all the files in the structure described above.
3.  Open your terminal or command prompt.
4.  Navigate to the `delivery_planner/` directory.
5.  Run the main script:
    ```bash
    python main.py
    ```
6.  The program will first display the optimal loading manifest and the delivery route.
7.  After that, it will prompt you to search for a package ID. You can enter an ID from the manifest (e.g., `PKG001`) or type `exit` to quit.