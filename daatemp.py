import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import networkx as nx
import osmnx as ox
import folium
import webbrowser
import json
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# ----------------------- Main Application Window -----------------------
root = tk.Tk()
root.title("Optimized Route Finder")
root.state("zoomed")  # Full screen
root.configure(bg='#E3F2FD')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# ----------------------- Global Graphs -----------------------
# Define the OSMnx graph globally for map route functionality.
# (If an error occurs here, a messagebox error is shown.)
try:
    graph_map = ox.graph_from_place("Haldwani, India", network_type="drive")
except Exception as e:
    messagebox.showerror("Error", f"Error loading map data: {e}")
    graph_map = None

# Global graph for manual entry data.
graph_manual = nx.Graph()

# ----------------------- Map-Based Route Finder Functions -----------------------
def find_map_route(start, end):
    """Finds the shortest route and calls visualize_map()."""
    if start and end and graph_map is not None:
        try:
            # Geocode returns a tuple (lat, lon)
            start_loc = ox.geocode(start)
            end_loc = ox.geocode(end)
            if not start_loc or not end_loc:
                messagebox.showerror("Error", "Could not geocode provided locations.")
                return
            # Nearest node function expects: x = longitude, y = latitude.
            start_node = ox.distance.nearest_nodes(graph_map, start_loc[1], start_loc[0])
            end_node = ox.distance.nearest_nodes(graph_map, end_loc[1], end_loc[0])
            path = nx.shortest_path(graph_map, source=start_node, target=end_node, weight="length")
            visualize_map(start_loc, end_loc, path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not find a route: {e}")
    else:
        messagebox.showerror("Error", "Please select both Start and Destination locations.")

def visualize_map(start_loc, end_loc, path):
    """Displays the shortest route on a Folium map."""
    route_coords = [(graph_map.nodes[node]['y'], graph_map.nodes[node]['x']) for node in path]
    route_map = folium.Map(location=route_coords[0], zoom_start=13)
    folium.Marker(location=start_loc, popup="Start", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(location=end_loc, popup="Destination", icon=folium.Icon(color="red")).add_to(route_map)
    folium.PolyLine(route_coords, color="blue", weight=5).add_to(route_map)
    map_path = "route_map.html"
    route_map.save(map_path)
    webbrowser.open(map_path)

# ----------------------- Manual Entry Functions -----------------------
def save_data():
    """Saves manual graph data to a JSON file."""
    file_path = filedialog.asksaveasfilename(defaultextension="DaaData.json",
                                             filetypes=[("JSON files", "*.json")])
    if file_path:
        data = {
            "nodes": list(graph_manual.nodes),
            "edges": [(u, v, d["weight"]) for u, v, d in graph_manual.edges(data=True)]
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)
        messagebox.showinfo("Info", "Data saved successfully!")

def update_data_display():
    """Update the listboxes with current graph data."""
    location_listbox.delete(0, tk.END)
    distance_listbox.delete(0, tk.END)

    for node in graph_manual.nodes:
        location_listbox.insert(tk.END, node)

    for u, v, d in graph_manual.edges(data=True):
        distance_listbox.insert(tk.END, f"{u} ↔ {v} : {d['weight']}")

# Container frame filling the whole window
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# ----------------------- Manual Entry Screen (Frame) -----------------------
frame_manual = tk.Frame(container)
frame_manual.place(relwidth=1, relheight=1)

# Load manual entry background image
try:
    manual_image = Image.open(r"manual.jpg")
    manual_image = manual_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    manual_bg_image = ImageTk.PhotoImage(manual_image)
    manual_bg_label = tk.Label(frame_manual, image=manual_bg_image)
    manual_bg_label.place(relwidth=1, relheight=1)
    manual_bg_label.image = manual_bg_image
except Exception as e:
    print("Error loading manual entry background image:", e)
    messagebox.showerror("Image Load Error", "Failed to load manual entry background image.")


manual_inner = tk.Frame(frame_manual, bg="#ffffff", padx=20, pady=20)  # Make sure this is defined before `add_frame`
manual_inner.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(manual_inner, text="Manual Route Entry", font=("Segoe UI", 16, "bold")).pack(pady=10)

# ----------------- Inline Add Section ----------------------
add_frame = tk.Frame(manual_inner, bg="#ffffff")
add_frame.pack(pady=10)

# --- Add Location ---
tk.Label(add_frame, text="Add Location:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, sticky="e")
location_entry = ttk.Entry(add_frame, width=25)
location_entry.grid(row=0, column=1, padx=5)

def add_location_inline():
    loc = location_entry.get().strip()
    if loc:
        if loc not in graph_manual.nodes:
            graph_manual.add_node(loc)
            update_data_display()
            location_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Location already exists.")
    else:
        messagebox.showerror("Error", "Please enter a location name.")


# --- Add Distance ---
tk.Label(add_frame, text="From:", font=("Arial", 11), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
from_entry = ttk.Entry(add_frame, width=15)
from_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(add_frame, text="To:", font=("Arial", 11), bg="#ffffff").grid(row=1, column=2, padx=5, pady=5, sticky="e")
to_entry = ttk.Entry(add_frame, width=15)
to_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(add_frame, text="Distance:", font=("Arial", 11), bg="#ffffff").grid(row=1, column=4, padx=5, sticky="e")
dist_entry = ttk.Entry(add_frame, width=10)
dist_entry.grid(row=1, column=5, padx=5)

def add_distance_inline():
    loc1 = from_entry.get().strip()
    loc2 = to_entry.get().strip()
    try:
        dist = float(dist_entry.get())
        if loc1 in graph_manual.nodes and loc2 in graph_manual.nodes:
            if dist > 0:
                graph_manual.add_edge(loc1, loc2, weight=dist)
                update_data_display()
                from_entry.delete(0, tk.END)
                to_entry.delete(0, tk.END)
                dist_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Distance must be a positive number.")
        else:
            messagebox.showerror("Error", "Both locations must exist.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for distance.")

def remove_location():
    """Removes a selected location from the graph and updates the display."""
    selection = location_listbox.curselection()
    if selection:
        location = location_listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirm", f"Remove location '{location}' and all its connections?")
        if confirm:
            graph_manual.remove_node(location)
            update_data_display()
    else:
        messagebox.showerror("Error", "Please select a location to remove.")

def remove_distance():
    """Removes a selected distance (edge) from the graph."""
    selection = distance_listbox.curselection()
    if selection:
        edge_text = distance_listbox.get(selection[0])
        try:
            # Parse the string like "A ↔ B : 10"
            parts = edge_text.split("↔")
            loc1 = parts[0].strip()
            rest = parts[1].strip().split(":")
            loc2 = rest[0].strip()

            if graph_manual.has_edge(loc1, loc2):
                confirm = messagebox.askyesno("Confirm", f"Remove distance between '{loc1}' and '{loc2}'?")
                if confirm:
                    graph_manual.remove_edge(loc1, loc2)
                    update_data_display()
            else:
                messagebox.showerror("Error", "Edge not found in graph.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse selected distance.\n{e}")
    else:
        messagebox.showerror("Error", "Please select a distance to remove.")


# --- Shortest Route Inline ---
tk.Label(add_frame, text="Start:", font=("Arial", 11), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
shortest_start_entry = ttk.Entry(add_frame, width=15)
shortest_start_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(add_frame, text="End:", font=("Arial", 11), bg="#ffffff").grid(row=2, column=2, padx=5, pady=5, sticky="e")
shortest_end_entry = ttk.Entry(add_frame, width=15)
shortest_end_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

def find_shortest_route_inline():
    start = shortest_start_entry.get().strip()
    end = shortest_end_entry.get().strip()
    if start in graph_manual.nodes and end in graph_manual.nodes:
        try:
            path = nx.shortest_path(graph_manual, source=start, target=end, weight='weight')
            cost = nx.shortest_path_length(graph_manual, source=start, target=end, weight='weight')
            messagebox.showinfo("Result", f"Shortest Path: {' → '.join(path)}\nDistance: {cost}")
            visualize_graph(highlight_path=path)
        except nx.NetworkXNoPath:
            messagebox.showerror("Error", "No path exists between these locations!")
    else:
        messagebox.showerror("Error", "Both locations must exist!")

def load_data():
    """Loads manual data from a JSON file."""
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "DaaData.json")])
    if file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)
        graph_manual.clear()
        graph_manual.add_nodes_from(data['nodes'])
        for u, v, weight in data['edges']:
            graph_manual.add_edge(u, v, weight=weight)
        update_data_display()

def visualize_graph(highlight_path=None):
    """Displays the graph with shortest path highlighted and edge weights shown."""
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph_manual)
    nx.draw(graph_manual, pos, with_labels=True, node_color='#64B5F6', 
            edge_color='gray', node_size=2000, font_size=10)
    
    edge_labels = {(u, v): graph_manual[u][v]['weight'] for u, v in graph_manual.edges()}
    nx.draw_networkx_edge_labels(graph_manual, pos, edge_labels=edge_labels, font_color='black')
    
    if highlight_path:
        edges = list(zip(highlight_path, highlight_path[1:]))
        nx.draw_networkx_edges(graph_manual, pos, edgelist=edges, edge_color='red', width=2)
    plt.title("Graph Visualization with Distances")
    plt.show()

# ----------------------- Style Customization -----------------------
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=10,
                background="#42A5F5", foreground="white", borderwidth=2)
style.map("TButton", background=[("active", "#1E88E5")])
style.configure("TLabel", font=("Segoe UI", 14), background='#E3F2FD')

# ----------------------- Home Screen (Frame) -----------------------
frame_home = tk.Frame(container)
frame_home.place(relwidth=1, relheight=1)

# Load home background image
try:
    home_image = Image.open(r"home.jpg")
    home_image = home_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    home_bg_image = ImageTk.PhotoImage(home_image)
    home_bg_label = tk.Label(frame_home, image=home_bg_image)
    home_bg_label.place(relwidth=1, relheight=1)
    home_bg_label.image = home_bg_image  # Prevent garbage collection
except Exception as e:
    print("Error loading home background image:", e)
    messagebox.showerror("Image Load Error", "Failed to load home background image.")

home_inner = tk.Frame(frame_home, bg="#ffffff", padx=50, pady=30)
home_inner.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(home_inner, text="Optimized Route Finder", font=("Segoe UI", 18, "bold")).pack(pady=20)
ttk.Button(home_inner, text="📍 Add Data Manually", command=lambda: show_frame(frame_manual)).pack(pady=10)
ttk.Button(home_inner, text="🗺️ Show Map Routes", command=lambda: show_frame(frame_map)).pack(pady=10)


# Two separate listboxes for clarity.
listbox_frame = tk.Frame(manual_inner, bg="#FAFAFA")
listbox_frame.pack(pady=10,  anchor="center")

tk.Label(listbox_frame, text="📍 Locations", font=("Arial", 12, "bold"), bg="#FAFAFA").grid(row=0, column=0, padx=10)
tk.Label(listbox_frame, text="🔗 Distances", font=("Arial", 12, "bold"), bg="#FAFAFA").grid(row=0, column=1, padx=10)

location_listbox = tk.Listbox(listbox_frame, width=30, height=10, font=("Arial", 11))
location_listbox.grid(row=1, column=0, padx=10)

distance_listbox = tk.Listbox(listbox_frame, width=50, height=10, font=("Arial", 11))
distance_listbox.grid(row=1, column=1, padx=10)

# Grouped buttons for manual entry operations.
button_frame = tk.Frame(manual_inner, bg="#ffffff")
button_frame.pack(pady=5)
graph_ops_frame = tk.Frame(manual_inner, bg="#ffffff")
graph_ops_frame.pack(pady=10)
ttk.Button(add_frame, text="➕ Add Location", command=add_location_inline).grid(row=0, column=2, padx=5)
ttk.Button(add_frame, text="🔗 Add Distance", command=add_distance_inline).grid(row=1, column=6, padx=5)
ttk.Button(button_frame, text="❌ Remove Location", command=remove_location).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="❌ Remove Distance", command=remove_distance).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(add_frame, text="🚗 Find Shortest Route", command=find_shortest_route_inline).grid(row=2, column=4, padx=5)
ttk.Button(graph_ops_frame, text="📊 Show Graph", command=visualize_graph).pack(side="left", padx=10)
ttk.Button(graph_ops_frame, text="💾 Save Data", command=save_data).pack(side="left", padx=10)
ttk.Button(graph_ops_frame, text="📂 Load Data", command=load_data).pack(side="left", padx=10)
ttk.Button(manual_inner, text="🔙 Back", command=lambda: show_frame(frame_home)).pack(pady=10)

# ----------------------- Map Screen (Frame) -----------------------
frame_map = tk.Frame(container)
frame_map.place(relwidth=1, relheight=1)

# Load map screen background image
try:
    map_image = Image.open(r"map.jpg")
    map_image = map_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    map_bg_image = ImageTk.PhotoImage(map_image)
    map_bg_label = tk.Label(frame_map, image=map_bg_image)
    map_bg_label.place(relwidth=1, relheight=1)
    map_bg_label.image = map_bg_image
except Exception as e:
    print("Error loading map background image:", e)
    messagebox.showerror("Image Load Error", "Failed to load map background image.")

map_inner = tk.Frame(frame_map, bg="#ffffff", padx=20, pady=20)
map_inner.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(map_inner, text="Map Route Finder", font=("Segoe UI", 16, "bold")).pack(pady=10)
locations = [
    "Haldwani", "Mall Road, Haldwani", "Bazaar Road, Haldwani",
    "Haldwani Railway Station", "Haldwani Bus Stand", "Gandhi Chowk, Haldwani",
    "Nainital Road, Haldwani", "Shivalik Colony, Haldwani", "Haldwani Medical College"
]
tk.Label(map_inner, text="From:", font=("Arial", 12), bg="#ffffff").pack(pady=(5, 0))
start_combobox = ttk.Combobox(map_inner, values=locations, width=40)
start_combobox.pack(pady=5)

tk.Label(map_inner, text="To:", font=("Arial", 12), bg="#ffffff").pack(pady=(5, 0))
dest_combobox = ttk.Combobox(map_inner, values=locations, width=40)
dest_combobox.pack(pady=5)

def find_map_route_safe():
    start = start_combobox.get().strip()
    destination = dest_combobox.get().strip()
    if not start or not destination:
        messagebox.showerror("Error", "Please select both Start and Destination locations")
    else:
        find_map_route(start, destination)

ttk.Button(map_inner, text="🚗 Find Map Route", command=find_map_route_safe)\
    .pack(pady=10)
ttk.Button(map_inner, text="🔙 Back", command=lambda: show_frame(frame_home))\
    .pack(pady=10)

# ----------------------- Navigation Helper -----------------------
def show_frame(frame):
    """Brings the given frame to the front."""
    frame.tkraise()

# Initially, show the Home Screen.
show_frame(frame_home)

# Run the application.
root.mainloop()
