import psutil
import time
import os

print("\n*** Please ensure that the target application is running ***\n")
time.sleep(1)

run = False

# Creates a directory for user data
os.makedirs("data/", exist_ok=True)

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

# Constant variables
loop = 0
file_loop = 0
file_list = []
file_app = ""
run = True

# Handling for data file
data_file_path = "data/app_time.txt"

if os.path.exists(data_file_path):
    ans = input("Continue from previous session (c) or reset to a new one? (r): ").lower()
    if ans == "c":
        with open(data_file_path, "r") as file:
            file_list = file.readlines()
            file_loop = int(file_list[0])
            file_app = file_list[1].rstrip('\n')
        print(f"Adding time to previous session(s) of {time_breakdown(file_loop)} in {file_app}")
    elif ans == "r":
        os.remove(data_file_path)
        flag = True
        while flag:
            file_app = input("What new app would you like to track? ")
            if is_exe(file_app, run):
                flag = False
            else:
                print("Please ensure that the target application is running")
    else:
        print("Error: Invalid user input. Press enter to exit and try again.")
        input()
        run = False
else:
    flag = True
    while flag:
        file_app = input("(Note: on windows, use the executable name rather than the app name; e.g., 'Spotify.exe' instead of 'Spotify')\nWhat app would you like to track? ")
        if is_exe(file_app, run):
            flag = False

with open(data_file_path, "w") as file:
    pass

# Main loop
while run:
    time.sleep(1)
    if is_exe(file_app, run):
        loop += 1
        if loop == 1:
            print(file_app + " is being tracked!")
        else:
            print('\r' + time_breakdown(loop) + " recorded this session", end="")
    elif loop >= 1:
        break

# Ask the user if they want to save data
if run:
    usr_in = input("\nSave data to 'data/app_time.txt'? (y/n): ")
    if usr_in.lower() != "n":
        with open(data_file_path, "w") as file:
            file.write(f"{file_loop+loop}\n{file_app}")
        print("Total project runtime: " + time_breakdown(file_loop+loop))
    elif usr_in.lower() not in ["y", "n"]:
        print("Warning: Bad user input, runtime was saved automatically")
        with open(data_file_path, "w") as file:
            file.write(f"{file_loop+loop}\n{file_app}")
    input("Press enter to exit")
