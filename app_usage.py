import psutil
import time
from os.path import exists
import os

if not exists("data/"):
    os.mkdir("data/")

def time_breakdown(secs):
    return str(int((secs)%(24*3600)/3600)) + " hours " + str(int((secs%3600)/60)) + " minutes and " + str((secs)%60) + " seconds"

loop = 0
file_loop = 0
file_list = []
file_app = ""
run = True

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
        os.remove("data/app_time.txt")
        file_app = input("What new app would you like to track? ")
        print("open " + file_app + " to begin tracking!")
    else:
        print("Error: invalid user input. Press enter to exit and try again.")
        input()
        run = False

else:
    file_app = input("(Note: use the executable name rather than the app name; i.e \'Resolve.exe\' instead of \'DaVinci Resolve\')\nWhat app would you like to track? ")
    file = open("app_time.txt", "w")
    print("open " + file_app + " to begin tracking!")

# main loop
while run:
    time.sleep(1)
    if (file_app in (i.name() for i in psutil.process_iter())):
        loop+=1
        if loop%1800 == 0:
            print(file_app + " has been running for " + time_breakdown(loop))
        elif loop == 1:
            print(file_app + " is being tracked!")
    elif (loop >= 1):
        print(time_breakdown(loop) + " have been recorded.")
        break
if run:
    usr_in = input("\nSave data? (y/n): ")
    if usr_in == "y":
        file = open("dataapp_time.txt", "w")
        print("total project runtime: " + time_breakdown(file_loop+loop))
        file.write(str(file_loop+loop) + "\n" + file_app)
    file.close()
    input("Press enter to exit")