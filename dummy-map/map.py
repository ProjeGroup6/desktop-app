# Read random points from socket and prints them
import socket
import threading
import pickle
import time


def receive_points(sock):
    import math
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.use("TkAgg")
    # Initialize empty lists to store x and y coordinates
    x_coordinates = []
    y_coordinates = []

    def update_graph():
        plt.scatter(
            x_coordinates, y_coordinates, color="red", s=10
        )  # Set the color and size of the points
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Graph")
        plt.draw()  # Update the graph without blocking the program
        plt.pause(0.001)  # Pause to allow the graph to be displayed

    # Handle point clicks
    def handle_click(event):
        if event.button == 1:  # Left mouse button
            clicked_point = (event.xdata, event.ydata)
            print("Clicked point:", clicked_point)

    # Create a figure and axis objects
    fig, ax = plt.subplots()

    # Connect the click event handler to the figure
    fig.canvas.mpl_connect("button_press_event", handle_click)

    while True:
        # read array
        data = sock.recv(1024)
        if not data:
            continue

        points = pickle.loads(data)

        # each index is an angle and points[index] is a distance
        for i in range(0, 360):
            # get x and y from angle and distance
            x = points[i] * math.cos(math.radians(i))
            y = points[i] * math.sin(math.radians(i))

            x_coordinates.append(x)
            y_coordinates.append(y)
            update_graph()


def start_client(address, port_points):
    points_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    points_socket.connect((address, port_points))
    print("Connected to server for points.")

    # Start a separate thread to receive points
    receive_points_thread = threading.Thread(
        target=receive_points, args=(points_socket,)
    )

    receive_points_thread.start()

    # Wait for the threads to finish
    receive_points_thread.join()

    print("Client connection closed.")
    points_socket.close()


server_address = input("Enter server address: ")
points_port = 8080
start_client(server_address, points_port)
