# Optimised-Route-Finder

🗺️ Optimised Route Finder

📖 Overview

This project, Optimised Route Finder, is built using Python with an intuitive Tkinter-based GUI for route visualization and analysis. It is designed to calculate and display the most efficient route between two given locations using graph-based shortest path algorithms. The system processes real-world geospatial data from OpenStreetMap (OSM) and constructs graph structures using NetworkX.

The application also integrates Folium for map rendering, allowing users to view start and end points, along with the optimized route, on an interactive map. It provides two modes: one for manual graph entry and another for real-world map-based routing. This project combines data visualization, geospatial computation, and algorithmic optimization within a simple and easy-to-use desktop interface.


---

🌟 Features

Built a Tkinter-based GUI for user-friendly interaction.

Uses Dijkstra’s algorithm for computing the shortest path.

Supports real-world map data through OpenStreetMap (OSM).

Displays interactive routes using Folium visualization.

Allows both manual graph entry and map-based path finding.

Exports and saves route data for later reference.



---

🧩 Tech Stack

Programming Language: Python

Libraries Used: Tkinter, NetworkX, Folium, OSMnx, JSON, Matplotlib

Algorithm: Dijkstra’s Shortest Path



---

🏗️ Project Structure

📂 Optimised-Route-Finder
│
├── 📄 daaproject.py       # Main file with Dijkstra algorithm and logic
├── 📄 dataempty.py        # Helper file for processing or initializing data
├── 📄 DataDatabase.json   # Data storage file for locations and connections
├── 📄 README.md           # Project documentation
├── 🖼️ home.jpg            # GUI home screen image
├── 🖼️ manual.jpg          # Manual graph entry image
├── 🖼️ map.jpg             # Map mode screenshot


---

⚙️ How to Run the Project

1️⃣ Clone the Repository

git clone https://github.com/<your-username>/Optimised-Route-Finder.git
cd Optimised-Route-Finder

2️⃣ Install Required Libraries

pip install networkx folium osmnx matplotlib

3️⃣ Run the Application

python daaproject.py

4️⃣ Use the App

Launches a Tkinter window.

Choose between Manual Mode or Map Mode.

In Map Mode: enter start and end locations → view optimized route on an interactive map.

In Manual Mode: input graph edges manually and view computed shortest path.



---

👨‍💻 Author

Priyanshu
B.Tech CSE (AI & ML) — Graphic Era Hill University, Bhimtal
📅 Project Duration: April 2025 – May 2025


---

🌟 Future Enhancements

Integrate real-time traffic data for smarter routing.

Add multiple route options and travel-time estimations.

Include PDF export of route summaries.

Add voice-based route input for accessibility.





> “Python-based route optimization tool using Tkinter, Folium, and Dijkstra’s algorithm.”
It’ll make your repository more visible and professional on GitHub.
