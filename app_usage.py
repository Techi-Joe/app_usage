import psutil
import time
from os.path import exists
import os

print("Please ensure that the target application is running")
time.sleep(1)

#creates a directory for user data
if not exists("data/"):
    os.mkdir("data/")

# checks if target executible is running
def is_exe(name):
    if (name in (i.name() for i in psutil.process_iter())):
        return True
    print("Error: Could not find running executable by name " + name)

# takes time in seconds and returns formatted string
def time_breakdown(secs):
    return str(int((secs)%(24*3600)/3600)) + " hours " + str(int((secs%3600)/60)) + " minutes and " + str((secs)%60) + " seconds"

#constant variables
loop = 0
file_loop = 0
file_list = []
file_app = ""
run = True

# Handling for data file
if exists("data/app_time.txt"):
    ans = input("Continue from previous session (c) or reset to a new one? (r): ")
    if ans == "c":
        file = open("data/app_time.txt", "r")
        file_list = file.readlines()
        file_loop = int(file_list[0])
        file_app = file_list[1]
        file.close()
        print("Adding time to previous session(s) of " + time_breakdown(file_loop) + " in " + file_app)
    elif ans == "r":
        file = open("data/app_time.txt", "w")
        file.write("")
        file.close()
        flag = True
        while flag:
            file_app = input("What new app would you like to track? ")
            if is_exe(file_app):
                flag = False
    else:
        print("Error: invalid user input. Press enter to exit and try again.")
        input()
        run = False
else:
    flag = True
    while flag:
        file_app = input("(Note: use the executable name rather than the app name; i.e \'Resolve.exe\' instead of \'DaVinci Resolve\')\nWhat app would you like to track? ")
        if is_exe(file_app):
            flag = False
    file = open("app_time.txt", "w")

# main loop
while run:
    time.sleep(1)
    if (file_app in (i.name() for i in psutil.process_iter())):
        loop+=1
        if loop == 1:
            print(file_app + " is being tracked!")
        else:
            print('\r' + time_breakdown(loop) + " recorded this session", end="")
    elif (loop >= 1):
        break

# ask user if they want to save data
if run:
    usr_in = input("\nSave data? (y/n): ")
    if not usr_in == "n":
        file = open("data/app_time.txt", "w")
        print("total project runtime: " + time_breakdown(file_loop+loop))
        file.write(str(file_loop+loop) + "\n" + file_app)
    elif not usr_in == "y" and not usr_in == "n":
        print("warning: bad user input, runtime was saved automatically")
    file.close()
    input("Press enter to exit")