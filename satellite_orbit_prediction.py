from skyfield.api import load, Topos
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def predict_satellite_position_at_time(satellite, initial_state, target_time, time_increment):
    ts = load.timescale()

    # Set the initial state
    satellite = satellite.at(target_time).from_xyz(
        initial_state[0] * 1000,  # Convert to meters
        initial_state[1] * 1000,
        initial_state[2] * 1000,
        initial_state[3] * 1000,  # Convert to meters/second
        initial_state[4] * 1000,
        initial_state[5] * 1000,
    )

    # Propagate the orbit forward to the target time
    final_state = satellite.at(target_time)

    return final_state.position().m, final_state.distance().m - 6371000  # Earth's radius in meters

def get_user_input():
    print("Enter initial conditions for the satellite:")
    x = float(input("x (km): "))
    y = float(input("y (km): "))
    z = float(input("z (km): "))
    vx = float(input("vx (km/s): "))
    vy = float(input("vy (km/s): "))
    vz = float(input("vz (km/s): "))

    # Get the target date
    target_date_str = input("\nEnter the target date in the format 'YYYY-MM-DD': ")
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

    # Get the target time
    target_time_str = input("Enter the target time in the format 'HH:MM:SS': ")
    target_time = datetime.strptime(target_time_str, "%H:%M:%S")

    # Combine date and time into a single datetime object
    target_time = target_date.replace(hour=target_time.hour, minute=target_time.minute, second=target_time.second)

    time_increment_seconds = float(input("Enter time increment between steps (seconds): "))

    return [x, y, z, vx, vy, vz], target_time, timedelta(seconds=time_increment_seconds)

def plot_satellite_orbit(positions):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract x, y, z coordinates for plotting
    x_coords = [position[0] for position in positions]
    y_coords = [position[1] for position in positions]
    z_coords = [position[2] for position in positions]

    # Create 3D scatter plot
    ax.plot(x_coords, y_coords, z_coords, label='Satellite Orbit')

    # Set plot labels
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')

    plt.legend()
    plt.show()

def main():
    print("Satellite Orbit Prediction Program")

    # Load satellite data
    satellites = load.tle_file("satellites.tle")

    # Get user inputs
    initial_state, target_time, time_increment = get_user_input()

    # Predict satellite positions at the target time
    positions = []
    for satellite in satellites:
        final_position, final_altitude = predict_satellite_position_at_time(satellite, initial_state, target_time, time_increment)
        positions.append(final_position)

    # Display results
    for i, position in enumerate(positions):
        print(f"\nPredicted Position of Satellite {i+1} at Target Time:", position)
        print("Predicted Altitude at Target Time:", final_altitude)

    # Plot the predicted orbits up to the target time
    plot_satellite_orbit(positions)

if __name__ == "__main__":
    main()
