# Quadruped Robot Controller

A Python-based quadruped robot control system with a GUI Interface to control positions for a quadruped robot. This system allows controlling the robot's servos using a graphical interface, saving and loading robot states, and communication with a microcontroller over serial.

## Table of Contents
- [Project Title and Description](#project-title-and-description)
- [Installation and Setup Instructions](#installation-and-setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Licenses](#licenses)

## Project Title and Description
This project is designed to control a quadruped robot using a set of servos. It includes:
- A GUI to control the servo positions.
- The ability to save and load robot states.
- Communication with a Raspberry Pi Pico W via serial and wifi using a WebREPL.

### Important Notes:
This has only been tested with:
- Visual Studio Code for the GUI (tkinter).
- Thonny for the micropython.
A Quadruped robot with 4 legs and 2 servos per leg is required to use this controller.

## Installation and Setup Instructions
1. Clone this repository.
```bash
git clone https://github.com/Heli202/Quadruped-RobotController.git
```
2. Install/Setup Dependences
- For the GUI (Tkinter)
  - `Tkinter` is typically pre-installed with Python, if not, enter the following:
    ```bash
    pip install tk
    ```
- For the serial/wifi communication (PySerial and WebREPL)
  ```bash
  pip install pyserial
  ```
  ```bash
  pip install webrepl
  ```
3. Connect the microcontroller to the PC with a cable.
4. Setup microcontroller environment
- Open Thonny and connect to the microcontroller using the COM port that is assinged to it (You can check device manager on Windows for this)
- Flash micropython onto the microcontroller.
- After connecting to the device, after the >>> type:
  ```bash
  import webrepl_setup
  ```
- It will ask you if you want to "(E)nable or (D)isable" it running on boot, enter `E` to enable. Set and confirm a password that you will remember for the WebREPL. Type `y` to reboot when asked.
- Transfer the `Quadruped_Thonny.py`, `boot.py` and `secrets.py` files onto the microcontroller.
## Usage Instructions
1. In Thonny, open the `secrets.py` and change the SSID and Password variables to the details of a WIFI connection you want to connect the microcontroller to.
2. Press Stop/Restart backend (Ctrl + F2) in Thonny to run the boot.py in order to connect to the WIFI and start the WebREPL. Take note of the IP address as you will need this later.
3. Now go to the "Configure Interpreter" option in Thonny and change from the COM connection to the WebREPL, you will need to enter the IP address it chose automatically.
