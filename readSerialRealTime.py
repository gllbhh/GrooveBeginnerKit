import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up serial connection (adjust the COM port and baud rate as needed)
serial_port = 'COM4'  # Change this to your serial port (e.g., '/dev/ttyUSB0' for Linux)
baud_rate = 9600      # Set this to the baud rate of your Arduino

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Initialize lists to store data
temperature_data = []
humidity_data = []
time_data = []

# Function to update the plot
def update_plot(frame):
    try:
        # Read data from the serial port
        line = ser.readline().decode('utf-8').strip()  # Read and decode the serial data
        
        if line:  # Make sure there's data
            try:
                # Parse the two float values from the line (separated by space)
                temperature, humidity = map(float, line.split())

                # Append the new data to lists
                temperature_data.append(temperature)
                humidity_data.append(humidity)
                time_data.append(len(time_data))  # Use length of time_data as a proxy for time

                # Limit the list size for smooth plotting (e.g., keep last 100 data points)
                temperature_data[:] = temperature_data[-100:]
                humidity_data[:] = humidity_data[-100:]
                time_data[:] = time_data[-100:]

                # Clear the previous plots
                plt.cla()

                # Plot the data
                plt.plot(time_data, temperature_data, label="Temperature (°C)", color='r')
                plt.plot(time_data, humidity_data, label="Humidity (%)", color='b')

                # Add labels and legend
                plt.xlabel('Time')
                plt.ylabel('Value')
                plt.legend(loc='upper right')

                # Set plot title
                plt.title('Real-Time Temperature and Humidity Data')

            except (ValueError, IndexError) as e:
                print(f"Error parsing data: {e}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        plt.close()  # Close the plot if there is a serial error (e.g., Arduino is disconnected)

# Set up the animation for real-time plotting
fig = plt.figure()
ani = FuncAnimation(fig, update_plot, interval=1000)  # Update every 1 second

# Show the plot
plt.tight_layout()
plt.show()

# Don't forget to close the serial connection when done
ser.close()
