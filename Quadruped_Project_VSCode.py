import tkinter as tk
from tkinter import *
from tkinter import messagebox
import json
import serial

# Have to figure out how to send and receive specific commands for serial
class Servo:
    """Represents a servo motor in the GUI."""
    
    def __init__(self, parent, servo_id, name: str, x: int, y: int, min_val=0, max_val=180):
        """Initialize a servo control in the GUI using the grid system with x and y coordinates."""
        self.parent = parent
        self.servo_id = servo_id
        self.name = name
        self.value = StringVar()

        self.label = Label(parent, text=self.name)
        self.label.grid(row=y, column=x, padx=10, pady=10)

        self.scale = Scale(parent, variable=self.value, from_=min_val, to=max_val, orient=HORIZONTAL, length=200)
        self.scale.grid(row=y, column=x + 1, padx=10, pady=10)

    def get_value(self):
        """Get the current value of the servo."""
        return self.value.get()

    def set_value(self, value):
        """Set the value of the servo."""
        self.value.set(value)

class Leg:
    """Represents a leg of the quadruped, composed of two servos."""
    
    def __init__(self, parent, leg_id, base_x, base_y):
        """Initialize a leg with two servos, using base_x and base_y as starting positions."""
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
            labels = ["BRH (Back Right Hip)" ,"BRA (Back Right Ankle)"]

        for servo_id in range(1, 3):
            servo_name = labels[servo_id - 1]
            base_y = base_y + (servo_id - 1)
            servo = Servo(parent, servo_id, servo_name, base_x, base_y)
            self.servos.append(servo)

class Quadruped:
    """Represents the entire quadruped robot."""
    
    def __init__(self, parent, default_servo_rotation=90):
        """Initialize the quadruped with four legs, placing them using base_x and base_y."""
        self.parent = parent
        self.legs = []
        
        for leg_id in range(1, 5):
            base_y = (leg_id - 1) % 2 * 2  # Each leg takes two rows

            if leg_id <= 2:
                base_x = 0  # Legs 1 and 2 on the left side
            else:
                base_x = 4  # Legs 3 and 4 on the right side

            leg = Leg(parent, leg_id, base_x, base_y)
            self.legs.append(leg)

    def get_all_positions(self):
        """Get positions of all servos in the quadruped."""

        pass

    def set_all_positions(self, positions):
        """Set positions of all servos in the quadruped."""

        pass

class StateManager:
    """Manages saving and loading of robot states."""
    def __init__(self):
        """Initialize the state manager."""
        self.filename = "states.json"
        self.states_dict = {}

    def load_states(self):
        """Load states from a file."""
        try:
            with open(self.filename, "r") as file:
                self.states_dict = json.load(file)
                print("Loaded states:", self.states_dict)
        except FileNotFoundError:
            print("States file not found, creating file with empty states...")
            self.save_states({}) # Save with empty dictionary if no file found
        except TypeError:
            print("There was an issue with the deserialising of the dictionary to python format.")
            
    def save_states(self, states):
        """Save states to a file."""
        self.states_dict.update(states)
        try:
            with open(self.filename, "w") as outfile:
                json.dump(self.states_dict, outfile)
                print("Saved states:", self.states_dict)
        except TypeError:
            print("There was an issue with serialising the dictionary to json format")
        
    def get_state(self, name: str):
        """Get a specific state by name."""
        if name in self.states_dict:
            return self.states_dict[name]
        return

    def set_state(self, name: str, state: str):
        """Set a specific state by name."""
        pass

class SerialCommunicator:
    """Handles serial communication with the Pico."""
    
    def __init__(self, port='COM6', baud_rate=115200):
        """Initialize the serial connection."""
        try:
            self.s = serial.Serial(port, baud_rate)
        except serial.SerialException:
            print("Couldn't find COM port")
            
    def send_command(self, command: str): # Need to figure out how to send specific / logic
        """Send a command to the Pico."""
        # self.s.write() # Will have to happen when the load state happens with the information from the json file, 
        # but also how would u know where they are when saving state??? perhaps it needs to happen when loading and when changing slider or just
        # when slider changes, but have the load change the sliders which in turn sends the command? *** Figure this out
        pass

    def receive_data(self):
        """Receive data from the Pico."""
        while True:
            if self.s.in_waiting > 0:
                message = self.s.readline().decode("utf-8").strip()
                return message
            return None

class QuadrupedGUI:
    """Main GUI class for controlling the quadruped robot."""
    
    def __init__(self, parent):
        """Initialize the GUI."""
        self.parent = parent
        self.parent.geometry("1200x600")
        self.parent.title("Quadruped GUI")
        self.state_manager = StateManager()
        self.quadruped = Quadruped(root)
        self.create_gui()

    def create_gui(self):
        """Create the GUI elements."""
        self.save_entry = Entry(self.parent, width=20)
        self.save_entry.grid(row=8, column=0)
        self.load_entry = Entry(self.parent, width=20)
        self.load_entry.grid(row=9, column=0)
        Button(self.parent, text="Save State", command=self.save_state).grid(row=8, column=1, padx=0, pady=0)
        Button(self.parent, text="Load State", command=self.load_state).grid(row=9, column=1, padx=10, pady=10)
        Button(self.parent, text="Send to Pico", command=self.update_pico).grid(row=8, column=5, padx=0, pady=20)
        Button(self.parent, text="Reset Scales", command=self.reset_scales).grid(row=9, column=2, padx=10, pady=10)


    def update_pico(self):
        """Send updated positions to the Pico.""" # Will need to use serial communicator
        pass

    def save_state(self):
        """Save the current state of the robot."""
        self.save_state_name = self.save_entry.get()
        if not self.save_state_name.strip():
            messagebox.showerror("Error", "Please enter a valid save state name")
            return
        states = {}
        for leg in self.quadruped.legs:
            for servo in leg.servos:
                states[servo.name] = servo.get_value()
        self.state_manager.save_states({self.save_state_name: states})
        

    def load_state(self):
        """Load the last saved state of the robot."""
        self.state_manager.load_states()
        load_state_name = self.load_entry.get()
        if not load_state_name.strip():
            messagebox.showerror("Error", "Please enter a valid load state name")
            return
        self.state_manager.load_states()
        try:
            state_data = self.state_manager.get_state(load_state_name)
            if state_data is None:
                messagebox.showerror("Error", "State name does not exist")
                return
            for leg in self.quadruped.legs:
                for servo in leg.servos:
                    if servo.name in state_data:
                        servo.set_value(state_data[servo.name])
                    else:
                        messagebox.showwarning("Warning", f"No value found for {servo.name} in the loaded state")
        except Exception:
            messagebox.showerror("Error", f"An error occured while loading the state: {load_state_name}")
    
    def reset_scales(self):
        """Reset each scale for tkinter GUI"""
        try:
            for leg in self.quadruped.legs:
                for servo in leg.servos:
                    servo.set_value(0)
            messagebox.showinfo("Notice", "All scales were reset")
        except:
            messagebox.showerror("Error", "There was an issue resetting the scales")



if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedGUI(root)
    root.mainloop()
