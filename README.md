
Advanced Delivery Planner

A web-based logistics tool that uses classic computer science algorithms to solve a real-world problem: optimizing delivery truck loads and calculating efficient routes. This application provides a clean, interactive user interface for planning daily delivery operations.

The application intelligently selects the most valuable packages for a given truck capacity and then calculates a valid round-trip route to all delivery destinations.

Core Features

Dynamic Planning: Enter a truck's weight capacity and get an optimized plan in seconds.

Optimal Package Selection: Uses the 0/1 Knapsack algorithm to determine the most valuable combination of packages to load onto the truck without exceeding its weight limit.

Efficient Route Calculation: Employs a Hamiltonian Cycle algorithm to find a valid round-trip route that starts at the warehouse, visits each unique delivery location exactly once, and returns.

Interactive Map Visualization: Displays the calculated route on an interactive map using Leaflet.js, with custom markers for the warehouse and delivery stops.

Modern Web Interface: Built with a clean, responsive frontend that communicates with a Flask backend via an API, ensuring a smooth user experience without page reloads.

Algorithms in Action

This project was built to demonstrate the practical application of fundamental algorithms:

1. 0/1 Knapsack Algorithm  .

Problem: A delivery truck has a fixed weight capacity. How do you select which packages to deliver from a list of available packages, each with its own weight and priority (value)?

Solution: The Knapsack algorithm is used to select the subset of packages that yields the maximum total priority while staying within the truck's weight capacity.

2. Hamiltonian Cycle Algorithm

Problem: Once the packages are loaded, the driver needs an efficient route that visits every destination exactly once before returning to the start.

Solution: The application constructs a graph where locations are vertices. A backtracking algorithm is then used to find a Hamiltonian Cycle—a closed loop that visits every vertex exactly once.

Note: This is an NP-complete problem. For performance reasons, a guardrail is implemented to limit the number of unique destinations for which a route can be calculated.

Tech Stack

Backend: Python 3, Flask

Frontend: HTML5, CSS3, JavaScript (ES6+)

Mapping Library: Leaflet.js

Algorithms: Implemented in pure Python.

Development: Virtual Environment (venv)

Project Structure
code
Code
download
content_copy
expand_less
.
├── algorithms/
│   ├── hamiltonian.py
│   └── knapsack.py
├── data/
│   ├── locations_with_coords.csv
│   └── packages.csv
├── static/
│   ├── css/style.css
│   ├── img/
│   │   ├── depot.png
│   │   └── package.png
│   └── js/main.js
├── templates/
│   └── index.html
├── app.py
├── data_loader.py
├── planner_logic.py
└── requirements.txt
Setup and Installation

Follow these steps to get the application running on your local machine.

Prerequisites

Python 3.8+

pip (Python package installer)

1. Prepare Project Folder

Ensure all the project files and folders are organized according to the structure above in a main directory (e.g., delivery_planner_final).

2. Create and Activate a Virtual Environment

Open your terminal or command prompt and navigate to the project's root directory.

On macOS / Linux:

code
Bash
download
content_copy
expand_less
python3 -m venv venv
source venv/bin/activate

On Windows:

code
Bash
download
content_copy
expand_less
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies

Install all the required Python packages from the requirements.txt file.

code
Bash
download
content_copy
expand_less
pip install -r requirements.txt
4. Run the Application

Start the Flask development server.

code
Bash
download
content_copy
expand_less
python app.py
5. Access the Application

Once the server is running, you will see output like this:

code
Code
download
content_copy
expand_less
* Running on http://127.0.0.1:5000
 * Press CTRL+C to quit

Open your web browser and navigate to http://127.0.0.1:5000.

How to Use

The application will load with a default truck capacity of 100 kg.

You can change this value to any positive number.

Click the "Generate Plan" button.

A loading animation will appear while the backend processes the request.

The results will be displayed in two cards:

Optimal Loading Manifest: A table showing the packages that should be loaded.

Optimal Delivery Route: The sequence of stops and an interactive map visualizing the route.

Troubleshooting

ImportError: cannot import name 'url_quote' from 'werkzeug.urls'

Cause: Incompatibility between Flask and newer versions of Werkzeug.

Solution: The requirements.txt file pins Werkzeug==2.3.8 to solve this. Ensure you have installed dependencies using pip install -r requirements.txt.

Address already in use or Port 5000 is in use

Cause: Another process (likely a previous, unstopped run of this app) is using port 5000.

Solution 1 (Recommended): Find and stop the old process. Search online for "how to kill a process on port 5000" for your specific operating system.

Solution 2 (Quick Fix): Run the app on a different port by modifying the last line of app.py to app.run(debug=True, port=5001).