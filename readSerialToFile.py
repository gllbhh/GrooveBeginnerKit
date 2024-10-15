'''
    Script that lists avaliable serial ports, 
    prompts user to select one and reads the input from the serial port 
    and saves it to a text file serial_data.txt
    in format:
    yyyy-mm-dd hh:mm:ss <temperature> <humidity>
    incoming data format:
    <temperature> <humidity>

    Requires package pyserial
    Run following command to install it:
    pip install pyserial

                By Gleb B. for Fab Lab Suomi Bootcamp

    press CRTL+C to stop the script
'''





# Import necessary libraries
from datetime import datetime  # For getting the current timestamp
import time  # For adding delays
import serial  # For serial communication
import serial.tools.list_ports  # For listing available COM ports

# Function to list all available COM ports
def list_serial_ports():
    '''list serial ports avaliable'''
    # Use the serial.tools.list_ports.comports() function to get a list of available COM ports
    ports = serial.tools.list_ports.comports()
    # Return a list of the device names for each available port
    return [port.device for port in ports]

# Function to prompt the user to select a COM port from the available list
def select_serial_port(available_ports):
    '''Print Com port list and ask user to select one'''
    print("Available COM ports:")
    # Display all available COM ports with an index number
    for i, port in enumerate(available_ports):
        print(f"{i + 1}: {port}")

    # Keep prompting the user until a valid choice is made
    while True:
        try:
            # Ask the user to select a COM port by its index number
            choice = int(input("Select a COM port by number: ")) - 1
            # Check if the choice is valid (within the range of available ports)
            if 0 <= choice < len(available_ports):
                # Return the selected COM port
                return available_ports[choice]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            # Handle cases where the input is not a valid integer
            print("Please enter a valid number.")

# Function to save the data received from the serial port to a file
def save_data_to_file(data, file):
    '''save data to file'''
    # Get the current timestamp in 'YYYY-MM-DD HH:MM:SS' format
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Write the timestamp and the received data to the file, separated by a tab
    file.write(f"{timestamp}\t{data}\n")
    # Flush the file buffer to ensure that the data is written immediately
    file.flush()

# Function to read and print data from the selected serial port, and save it to a file
def read_serial_data(ser, filename):
    '''read data from the serial port'''
    print(f"Reading data from the serial port and saving to {filename}...")
    
    # Open the specified file in append mode to avoid overwriting existing data
    with open(filename, 'a') as file:
        try:
            # Continuously read data from the serial port
            while True:
                # Check if there is data waiting in the serial input buffer
                if ser.in_waiting > 0:
                    # Read a line of data from the serial port, decode it, and strip any extra whitespace
                    data = ser.readline().decode('utf-8').strip()
                    # Print the received data to the console
                    print(f"Received: {data}")
                    
                    # Save the received data to the file
                    save_data_to_file(data, file)
                
                # Add a small delay to avoid using too much CPU
                time.sleep(0.1)
        except KeyboardInterrupt:
            # Handle the user pressing Ctrl+C to stop the serial reading process
            print("\nSerial reading stopped by user.")

# Main function
def main():
    '''main'''
    # Get the list of available COM ports
    available_ports = list_serial_ports()
    
    # If no COM ports are available, print a message and exit the program
    if not available_ports:
        print("No COM ports available.")
        return
    
    # Ask the user to select a COM port from the available list
    selected_port = select_serial_port(available_ports)
    
    # Try to open the selected serial port with a baud rate of 9600
    try:
        # Open the serial port with the specified baud rate and a timeout of 1 second
        ser = serial.Serial(selected_port, 9600, timeout=1)
        print(f"Opened {selected_port} successfully.")
    except serial.SerialException as e:
        # If the port fails to open, print an error message and exit the program
        print(f"Failed to open {selected_port}: {e}")
        return

    # Define the filename where the serial data will be saved
    filename = 'serial_data.txt'

    # Start reading data from the serial port and saving it to the file
    read_serial_data(ser, filename)

    # Close the serial port when done
    ser.close()
    print(f"Closed {selected_port}.")

# Check if the script is being run directly (and not imported as a module)
if __name__ == "__main__":
    # Run the main function
    main()
