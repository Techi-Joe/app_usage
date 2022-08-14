import psutil
import time
import pickle
loop = 0

file = open("app_time.txt", "w")

while True:
    time.sleep(3)
    if ("Resolve.exe" in (i.name() for i in psutil.process_iter())):
        loop+=1
        print("Resolve.exe is running!")
    elif (loop >= 1):
        print(str(loop) + " minutes have been recorded.")
        break
input("\ndump data? (y/n): ")
if input == "y":
    pickle.dump(loop, file)
file.close()
with open('app_time.txt', 'rb') as f:
    file_loop = pickle.load(f)