import tkinter as tk
from tkinter import (
    messagebox, Label, Scale, StringVar, Button, Entry, HORIZONTAL
)

import json
import serial


class Servo:
    """
    Represents a servo motor in the GUI.

    Allows for control of the angle of each servo through a scale widget.

    Attributes:
        parent (tk.Widget): References the root for the tkinter window.
        servo_id (int): Unique identifier for the servo.
        name (str): Name reference for Labels, unique to each servo.
        x (int): The x-coordinate for grid placement.
        y (int): The y-coordinate for grid placement.
        min_val (int): Minimum angle value for the servo.
        max_val (int): Maximum angle value for the servo.
    """

    def __init__(self, parent, servo_id, name: str, x: int, y: int,
                 min_val=0, max_val=180):
        """Initialize a servo control (Scale) in the GUI using the grid system
        with x and y coordinates."""
        self.parent = parent
        self.servo_id = servo_id
        self.name = name
        self.value = StringVar()
        self.label = Label(parent, text=self.name)
        self.label.grid(row=y, column=x, padx=10, pady=10)
        self.scale = Scale(parent, variable=self.value, from_=min_val,
                           to=max_val, orient=HORIZONTAL, length=200)
        self.scale.grid(row=y, column=x + 1, padx=10, pady=10)

    def get_value(self):
        """Get the current value of the servo."""
        return self.value.get()

    def set_value(self, value):
        """Set the value of the servo."""
        self.scale.set(value)


class Leg:
    """Represents a leg of the quadruped, composed of two servos
    for movement control.

    Attributes:
        parent (tk.Widget): References the root for the tkinter window.
        leg_id (int): Unique identifier for the leg.
        servos (list[Servo]): List containing two Servo objects, representing
          hip and ankle.
    """

    def __init__(self, parent, leg_id, base_x, base_y):
        """Initialize each leg with two servos for hip and ankle"""
        self.parent = parent
        self.leg_id = leg_id
        self.servos = []

        if leg_id == 1:
            labels = ["FLH (Front Left Hip)", "FLA (Front Left Ankle)"]
        elif leg_id == 2:
            labels = ["FRH (Front Right Hip)", "FRA (Front Right Ankle)"]
        elif leg_id == 3:
            labels = ["BLH (Back Left Hip)", "BLA (Back Left Ankle)"]
        elif leg_id == 4:
            labels = ["BRH (Back Right Hip)", "BRA (Back Right Ankle)"]
        for servo_id in range(1, 3):
            servo_name = labels[servo_id - 1]
            base_y = base_y + (servo_id - 1)
            servo = Servo(parent, servo_id, servo_name, base_x, base_y)
            self.servos.append(servo)


class Quadruped:
    """Represents the entire quadruped robot composed of four legs.

    Attributes:
        parent (tk.Widget): References the root for the tkinter window.
        legs (list[Leg]): List of Leg objects, each representing a leg with
          two servos.
    """

    def __init__(self, parent):
        """Initialize the quadruped with four legs.

        Places legs using base_x and base_y to place them on
        a grid in the GUI.
        """
        self.parent = parent
        self.legs = []

        for leg_id in range(1, 5):
            base_y = (leg_id - 1) % 2 * 2  # Each leg takes two rows in the
            # GUI, odd on the left, even on the right

            if leg_id <= 2:
                base_x = 0
            else:
                base_x = 4

            leg = Leg(parent, leg_id, base_x, base_y)
            self.legs.append(leg)


class StateManager:
    """Manages saving and loading of robot states to and from
      a JSON file.

    Attributes:
        filename (str): Name of the file for storing the states.
        states_dict (dict): Dictionary containing saved states with names as
          keys.
        quadruped (Quadruped): The Quadruped instance whose state is managed.
    """

    def __init__(self, quadruped):
        """Initialize the state manager."""
        self.filename = "states.json"
        self.states_dict = {}
        self.quadruped = quadruped

    def load_states(self):
        """Load states from a file.

        Raises:
            FileNotFoundError: When the states.json doesn't exist.
            TypeError: If there is an issue deserialising the dictionary from
              the json file.
        """
        try:
            with open(self.filename, "r") as file:
                self.states_dict = json.load(file)
        except FileNotFoundError:
            print("States file not found, creating file with empty states...")
            self.save_states({})
        except TypeError:
            print("There was an issue with the deserialising of the\
            dictionary to python format.")

    def save_states(self, states_dict):
        """Save states to a file.

        Args:
            states_dict: Dictionary containing states that is passed back from
              the GUI.

        Raises:
            TypeError: If there is an issue serialising the dictionary to
              json format
        """
        self.states_dict.update(states_dict)
        try:
            with open(self.filename, "w") as outfile:
                json.dump(self.states_dict, outfile)
        except TypeError:
            print("There was an issue with serialising the dictionary to json\
            format")

    def get_state(self, name: str):
        """Returns a specific state by name."""
        if name in self.states_dict:
            return self.states_dict[name]
        return

    def set_state(self, state: str):
        """Set a specific state by name."""
        if state is None:
            print("State does not exist")
            return
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                if servo.name in state:
                    servo.set_value(state[servo.name])
                else:
                    print(f"No value found for {servo.name} in loaded state")


class SerialCommunicator:
    """Handles serial communication with the Pico microcontroller.

    Attributes:
        s (serial.Serial): Serial connection for sending and receiving data.
    """

    def __init__(self, port="COM6", baud_rate=115200):
        """Initialize the serial connection with the specified port and baud
          rate.

        Args:
            port (str): The COM port for the serial communication,
              e.g., "COM6".
            baud_rate (int): The baud rate for the serial connection.

        Raises:
            serial.SerialException: If the specified COM port isn't being used
              by the computer.
        """
        try:
            self.s = serial.Serial(port, baud_rate)
            print(f"Connected to {port} at {baud_rate} baud")
        except serial.SerialException:
            print("Couldn't find COM port")

    def send_command(self, value_list):
        """Send a command to the Pico.

        Args:
            command: Holds the comma seperated values converted to strings.
            commandbytes: Bytes version of the comma seperated values.

        Raises:
            AttributeError: If the COM port is already in use.
        """
        try:
            command = ",".join(map(str, value_list))
            commandbytes = bytes(f"{command}\n", encoding="utf-8")
            self.s.write(commandbytes)
            print(f"Command sent: {commandbytes}")
        except AttributeError:
            print("The COM port was already occupied")

    def receive_data(self):
        """Returns data received from the Pico."""
        while True:
            if self.s.in_waiting > 0:
                message = self.s.readline().decode("utf-8").strip()
                return message
            return None


class QuadrupedGUI:
    """Main tkinter GUI class for controlling the quadruped robot.

    Attributes:
        parent (tk.Widget): References the root for the tkinter window.
        quadruped (Quadruped): The main Quadruped object representing the
          robot.
        state_manager (StateManager): Initialises StateManager class.
        serial_communicator (SerialCommunicator): Initialises
          SerialCommunicator class.
    """

    def __init__(self, parent):
        """Initialize the GUI."""
        self.parent = parent
        self.parent.geometry("1200x600")
        self.parent.title("Quadruped GUI")
        self.quadruped = Quadruped(root)
        self.state_manager = StateManager(self.quadruped)
        self.serial_communicator = SerialCommunicator()
        self.create_gui()

    def create_gui(self):
        """Create the tkinter GUI elements."""
        self.save_entry = Entry(self.parent, width=20)
        self.save_entry.grid(row=8, column=0)
        self.load_entry = Entry(self.parent, width=20)
        self.load_entry.grid(row=9, column=0)
        Button(self.parent, text="Save State", command=self.save_state)\
            .grid(row=8, column=1, padx=0, pady=0)
        Button(self.parent, text="Load State", command=self.load_state)\
            .grid(row=9, column=1, padx=10, pady=10)
        Button(self.parent, text="Send to Pico", command=self.update_pico)\
            .grid(row=8, column=5, padx=0, pady=20)
        Button(self.parent, text="Reset Scales", command=self.reset_scales)\
            .grid(row=9, column=2, padx=10, pady=10)

    def update_pico(self):
        """Send updated positions to the Pico.

        Args:
            value_list: List to hold positions of servos.
            value: Holds value from a servo.
        """
        value_list = []
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                value = servo.get_value()
                value_list.append(value)
        self.serial_communicator.send_command(value_list)

    def save_state(self):
        """Save the current state of the robot.

        Args:
            save_state_name: Holds the name that the user inputs for
              saving state.
            states: A dictionary containing lists of states.
        """
        self.save_state_name = self.save_entry.get()
        if not self.save_state_name.strip():
            messagebox.showerror(
                "Error",
                "Please enter a valid save state name"
                )
            return
        states = {}
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                states[servo.name] = servo.get_value()
        self.state_manager.states_dict[self.save_state_name] = states
        self.state_manager.save_states(self.state_manager.states_dict)

    def load_state(self):
        """Load the last saved state of the robot.

        Args:
            load_state_name: Holds the name that the user inputs for
              loading state.
            state: Contains the input name after checking if it exists.

        Raises:
            AttributeError: If the state does not exist.
        """
        self.state_manager.load_states()
        load_state_name = self.load_entry.get()
        if not load_state_name.strip():
            messagebox.showerror(
                "Error",
                "Please enter a valid load state name"
                )
            return
        self.state_manager.load_states()
        try:
            state = self.state_manager.get_state(load_state_name)
            self.state_manager.set_state(state)
        except AttributeError:
            messagebox.showerror(
                "Error",
                f"The state name does not exist: {load_state_name}"
                )

    def reset_scales(self):
        """Reset each scale for tkinter GUI"""
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                servo.set_value(0)
        messagebox.showinfo(
            "Notice",
            "All scales were reset"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedGUI(root)
    root.mainloop()
