# Quadruped Robot Controller

A Python-based quadruped robot control system with a GUI Interface to control positions for a quadruped robot. This system allows controlling the robot's servos using a graphical interface, saving and loading robot states, and communication with a microcontroller over serial and remotely with Wi-Fi.

### Important Notes:
This has only been tested with:
- Visual Studio Code for the GUI, with Python (tkinter).
- Thonny for micropython.
**Required hardware** A Quadruped robot with 4 legs and 2 servos per leg is required to use this controller.

## Table of Contents
- [Project Title and Description](#project-title-and-description)
- [Installation and Setup Instructions](#installation-and-setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Licenses](#licenses)
- [External Libraries](#external-libraries)

## Project Title and Description
This project is designed to control a quadruped robot using a set of servos. It includes:
- A GUI to control the servo positions.
- The ability to save and load robot states.
- Communication with a Raspberry Pi Pico W via serial and wifi using a WebREPL.

## Installation and Setup Instructions
1. Clone this repository:
```bash
git clone https://github.com/Heli202/Quadruped-RobotController.git
```
2. Install/Setup Dependences:
- Ensure Python is installed on your system.
- Tkinter should be installed with Python, if not it will need to be installed seperately.
- Thonny: Install the required dependencies listed in `thonny_requirements.txt`:
```bash
pip install -r thonny_requirements.txt
```
- VSCode: Install the require dependencies listen in `vscode_requirements.txt`:
```bash
pip install -r vscode_requirements.txt
```
3. Setup microcontroller environment:
- Connect the microcontroller to you PC via USB.
- Open Thonny, then go to **Tools > Options > Interpreter** and select the appropriate COM port for your microcontroller. You can check the assigned COM port in the **Device Manager** (on Windows).
- Flash micropython onto the microcontroller if it's not already installed.
- In Thonny, at the `>>>` prompt, type:
  ```bash
  import webrepl_setup
  ```
- When prompted, choose (E)nable to enable WebREPL on boot, then set and confirm a password. Type y to reboot.

4. Transfer necessary files to the microcontroller:
- Upload `Quadruped_Thonny.py`, `boot.py` and `secrets.py` files onto the microcontroller.

5. Configure Wi-Fi credentials:
- In Thonny, open the `secrets.py` and set the SSID and Password variables to the details of the desired Wi-Fi network.

6. Start WebREPL:
- Press **Stop/Restart backend** (Ctrl + F2) in Thonny to run boot.py, connecting the micronctroller to Wi-Fi and starting WebREPL. Note the IP address displayed.

7. Connect Thonny to WebREPL:
- In Thonny, go to **Configure Interpreter**, switch from the COM connection to WebREPL, and enter the IP address and password from the setup. Afterwards you may need to **Stop/Restart backend** again for Thonny to switch over.
- Once `WebREPL connected` appears, Thonny is ready.

8. Open the GUI:
- Now open `Quadruped_PC` to launch the GUI.

## Usage Instructions
- From the GUI you now have the following controls:
### Scale Controls
- Control the **Scales** to adjust the degrees for servo movement.
- `Reset Scales` to reset all Scales to 0.
### State Control
- `Save State` and `Load State` buttons allow you to save and load configurations, with entry fields for naming each state.
### Command Control
- `Send to Pico` sends a command to the Pico, moving it to the current Scale values.

### Demo Video (showcasing functionality):
![Demo Video](https://img.youtube.com/vi/hOMUS9vagQ8/0.jpg)

[Watch the video](https://youtu.be/hOMUS9vagQ8)

## Licenses
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## External Libraries
This project uses the following external libraries:
- **Tkinter** - used for GUI development (Standard Library in Python, governed by Python's PSF License).
- **PySerial** - Check their [Repository](https://github.com/pyserial/pyserial) for more info.
  - License: [PSF License](https://opensource.org/license/python-2-0)
- **WebREPL** - Check their [Repository](https://github.com/micropython/webrepl) for more info.
  - License: [MIT License](https://opensource.org/licenses/MIT)