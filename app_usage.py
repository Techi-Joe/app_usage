"""
App Usage
=========

This script tracks the usage time of a specified application. 
It monitors the running time of the application
and saves the session data to a file. 
The script can also continue from a previous session.

Features:
---------
- Checks if the specified application is running.
- Records the running time of the application.
- Saves session data to a file.
- Allows continuation from a previous session.
- Provides a user-friendly interface to select or add new applications to track.

Usage:
------
1. Ensure the target application is running.
2. Run the script.
3. Choose to continue from a previous session or start a new one.
4. The script will monitor the application and record the running time.
5. Optionally save the session data when exiting.

Modules Required:
-----------------
- glob: for file pattern matching.
- psutil: for process management.
- time: for time tracking and sleeping.
- os: for operating system dependent functionality.
- sys: for system-specific parameters and functions.

Functions:
----------
- clear(): Clears the terminal screen.
- name_from_exe(exename): Parses executable filename to give just the name.
- any_data_file_exists(directory): Checks if any data file exists in the directory.
- parse_data_file(directory): Parses data files into a dictionary.
- is_exe(name, run): Checks if the target executable is running.
- time_breakdown(secs): Takes time in seconds and returns a formatted string.

Author:
-------
Techi-Joe

License:
--------
This project is licensed under the GPL-3.0 License.
"""

import glob
import psutil
import time
import os
import sys


#----------------------------------------------------------------
# Define variables

recorded_seconds = 0
file_time = 0
file_list = []
file_app = ""
run = True
data_file = ""
data_file_dir = "data/"

# appname : time
file_dict = {}

# Creates a directory for user data
os.makedirs(data_file_dir, exist_ok=True)

print("\n*** Please ensure that the target application is running ***\n")
time.sleep(1)

#----------------------------------------------------------------
# functions

# clear the terminal
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# parses exe filename to give just the name
def name_from_exe(exename):
    if os.name == 'nt' or exename.endswith('.app'):
        # Split on the last period to avoid issues with multiple periods in the name
        split_exe_name, exe = exename.rsplit('.', 1)
        return split_exe_name
    # On Unix-like systems, return the name as is, unless it is .app
    return exename

# Checks if any data file exists in the directory
def any_data_file_exists(directory):
    return bool(glob.glob(os.path.join(directory, '*.dat')))

# parses data files into a dictionary
def parse_data_file(directory):
    global file_dict
    for file in glob.glob(os.path.join(directory, '*.dat')):
        with open(file, "r") as f:
            lines = f.readlines()
            if len(lines) == 2:
                app_name = lines[1].strip()
                try:
                    app_time = int(lines[0].strip())
                except ValueError:
                    print(f"Error parsing time in {file}. Resetting to 0 seconds.")
                    app_time = 0
                file_dict[app_name] = app_time
            else:
                print(f"Error parsing data file: {file}")
                os.remove(file)
                print(f"{file} was deleted.")

# Checks if target executable is running
def is_exe(name, run):
    for process in psutil.process_iter(['name']):
        if name == process.info['name']:
            return True
    if run == False:
        print("Error: Could not find running executable by name " + name)

# Takes time in seconds and returns a formatted string
def time_breakdown(secs):
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hours {minutes} minutes and {seconds} seconds"

#----------------------------------------------------------------
# data file handling

if any_data_file_exists(data_file_dir):
    parse_data_file(data_file_dir)
    if len(file_dict) > 0:
        ans = input("Continue from a previous session (c) or start a new one (n)? ").lower()
    else:
        ans = "n"

    if ans == "c":
        clear()
        # Let user choose which app to continue
        print("Available sessions to continue:")

        for app in file_dict:
            print(f"- {app}: {time_breakdown(int(file_dict[app]))} on record")
        file_app = input("\nWhich app would you like to continue tracking? ")

        if file_app in file_dict:
            file_time = file_dict[file_app]
            data_file = f"{data_file_dir}{file_app}_data.dat"
        else:
            print("Error: App not found.")
            ans = "n"

    elif ans == "n" or file_app == "":
        flag = True

        while flag:
            file_app = input("What app would you like to track? ")

            if file_app in file_dict.keys():
                erase_q = input("You have a previous session of this application on record. Do you want to erase it? (y/n): ").lower()
                if erase_q in ["y", "n"]:
                    if erase_q == "y":
                        os.remove(f"{data_file_dir}{name_from_exe(file_app)}_data.dat")
                    else:
                        input("To continue with your previous session, please restart App Usage. Press enter to exit.")
                        sys.exit()
                else:
                    input("Error: not a valid response. Defaulting to no. Press enter to exit.")
                    sys.exit(1)

            if is_exe(file_app, run):
                flag = False
                data_file = f"{data_file_dir}{name_from_exe(file_app)}_data.dat"
            else:
                print("Please ensure that the target application is running")
    else:
        input("Error: Invalid user input. Press enter to exit and try again.")
        sys.exit(1)
else:
    flag = True

    while flag:

        if os.name == "nt":
            print("Note: on windows, use the executable name rather than the app name; e.g., \'app_usage-2.0.exe\' instead of \'App Usage\'. Sometimes this name is different from the one that appears in the system tray.")

        file_app = input("\nWhat app would you like to track? ")
        if is_exe(file_app, run):
            flag = False
            data_file = f"{data_file_dir}{name_from_exe(file_app)}_data.dat"

try:
    with open(data_file, "w") as file:
        pass
except FileNotFoundError:
    input("Data file not found or was corrupted. Press enter to exit.")
    sys.exit(1)

clear()

#----------------------------------------------------------------
# main code loop

start_time = time.time()
while run:
    current_time = time.time()
    elapsed_time = round(current_time - start_time)
    if is_exe(file_app, run):
        if elapsed_time > recorded_seconds:
            recorded_seconds += 1
            if recorded_seconds == 1:
                start_time = time.time()
                print(file_app + " is being tracked!")
        elif recorded_seconds > 0:
            print('\r' + time_breakdown(recorded_seconds) + " recorded", end="  \r")
    elif recorded_seconds >= 1:
        break

    time.sleep(1)

# Ask the user if they want to save data
if run:
    usr_in = input(f"\nSave data to '{data_file}'? (y/n): ")
    if usr_in.lower() != "n":
        with open(data_file, "w") as file:
            file.write(f"{file_time+recorded_seconds}\n{file_app}")
        print("Total session runtime: " + time_breakdown(file_time+recorded_seconds))
    elif usr_in.lower() not in ["y", "n"]:
        print("Warning: Bad user input, runtime was saved automatically")
        with open(data_file, "w") as file:
            file.write(f"{file_time+recorded_seconds}\n{file_app}")
    else:
        with open(data_file, "w") as file:
            file.write(f"{file_time}\n{file_app}")
    input("Press enter to exit")
