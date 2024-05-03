from skyfield.api import load, Topos
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def test_predict_satellite_position_at_time():
    # Define a sample satellite state and target time
    initial_state = [0, 0, 0, 1, 1, 1]  # x, y, z, vx, vy, vz in km and km/s
    target_time = datetime(2024, 5, 3, 12, 0, 0)  # May 3rd, 2024, 12:00:00 PM

    # Load satellite data
    satellites = load.tle_file("satellites.tle")

    # Test predict_satellite_position_at_time function
    for satellite in satellites:
        final_position, final_altitude = predict_satellite_position_at_time(satellite, initial_state, target_time, timedelta(seconds=60))
        assert isinstance(final_position, tuple)
        assert len(final_position) == 3
        assert isinstance(final_altitude, float)

def test_get_user_input():
    # Mock user input
    user_input = [
        "0", "0", "0",  # x, y, z
        "1", "1", "1",  # vx, vy, vz
        "2024-05-03", "12:00:00",  # target date and time
        "60"  # time increment in seconds
    ]
    expected_output = ([0.0, 0.0, 0.0, 1.0, 1.0, 1.0], datetime(2024, 5, 3, 12, 0, 0), timedelta(seconds=60))

    # Redirect input to mock user input
    original_input = __builtins__.input
    __builtins__.input = lambda _: user_input.pop(0)

    # Test get_user_input function
    assert get_user_input() == expected_output

    # Restore original input function
    __builtins__.input = original_input

def test_plot_satellite_orbit():
    # Sample positions
    positions = [(0, 0, 0), (1000, 1000, 1000), (-1000, -1000, -1000)]

    # Test plot_satellite_orbit function
    plot_satellite_orbit(positions)

def test_main():
    # Test main function
    main()

if __name__ == "__main__":
    test_predict_satellite_position_at_time()
    test_get_user_input()
    test_plot_satellite_orbit()
    test_main()
    print("All tests passed successfully!")
