import glob
import psutil
import time
import os

print("\n*** Please ensure that the target application is running ***\n")
time.sleep(1)

run = False

# Checks if any text file exists in the directory
def any_text_file_exists(directory):
    return bool(glob.glob(os.path.join(directory, '*.txt')))

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
recorded_seconds = 0
file_time = 0
file_list = []
file_app = ""
run = True
data_file = ""

# Handling for data file
data_file_dir = "data/"

if any_text_file_exists(data_file_dir):
    ans = input("Continue from previous session (c) or start to a new one? (n): ").lower()
    if ans == "c":
        with open(data_file, "r") as file:
            file_list = file.readlines()
            file_time = int(file_list[0])
            file_app = file_list[1].rstrip('\n')
        print(f"Adding time to previous session(s) of {time_breakdown(file_time)} in {file_app}")
    elif ans == "n":
        os.remove(data_file)
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
        file_app = input("(Note: on windows, use the executable name rather than the app name; e.g., 'Spotify.exe' instead of 'Spotify')\n\nWhat app would you like to track? ")
        if is_exe(file_app, run):
            flag = False
            data_file = f"{data_file_dir}/{file_app}_data.txt"

with open(data_file, "w") as file:
    pass

start_time = time.time()
# Main loop
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
            print('\r' + time_breakdown(recorded_seconds) + " recorded this session", end="")
    elif recorded_seconds >= 1:
        break

# Ask the user if they want to save data
if run:
    usr_in = input(f"\nSave data to '{data_file}'? (y/n): ")
    if usr_in.lower() != "n":
        with open(data_file, "w") as file:
            file.write(f"{file_time+recorded_seconds}\n{file_app}")
        print("Total project runtime: " + time_breakdown(file_time+recorded_seconds))
    elif usr_in.lower() not in ["y", "n"]:
        print("Warning: Bad user input, runtime was saved automatically")
        with open(data_file, "w") as file:
            file.write(f"{file_time+recorded_seconds}\n{file_app}")
    input("Press enter to exit")
