import psutil
import time
from os.path import exists
loop = 0
file_loop = 0
if exists("app_time.txt"):
    file = open("app_time.txt", "r")
    file_loop = int(file.read())
    file.close()
else:
    file = open("app_time.txt", "w")
while True:
    time.sleep(1)
    if ("Spotify.exe" in (i.name() for i in psutil.process_iter())):
        loop+=1
        print("Spotify.exe is running!")
    elif (loop >= 1):
        print(str(loop) + " minutes have been recorded.")
        break
usr_in = input("\nSave data? (y/n): ")
if usr_in == "y":
    file = open("app_time.txt", "w")
    print(str(file_loop+loop) + " total minutes")
    file.write(str(file_loop+loop))
file.close()