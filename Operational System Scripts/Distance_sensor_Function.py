import busio
import board
from adafruit_vl53l0x import VL53L0X
import statistics

# Set up the I2C and VL53L0X sensor
i2c = busio.I2C(board.SCL, board.SDA)
tof = VL53L0X(i2c)

distance_values = []

def measure_distance(label):
    global median_distance
    # Perform distance measurement and return the distance in mm
    tof.measurement_timing_budget = 200000
    distance_mm = tof.range

    # Append the distance to the list
    distance_values.append(distance_mm)

    # Check if we have collected 5 distance values
    if len(distance_values) == 5:
        # Calculate the median of the collected distance values with offset (39 mm)
        median_distance = statistics.median(distance_values) - 39
        
        # Clear the list for the next 5 measurements
        distance_values.clear()
        
        # Update the label with the mean distance value
        label.config(text="Distance from bottom: {} mm".format(median_distance))

    # Schedule the next measurement after 1 second
    label.after(1000, measure_distance, label)



