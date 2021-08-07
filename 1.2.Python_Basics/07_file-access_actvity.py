# 1.2.6.4: Activity – Create a Script to Allow User to Add Devices

file = open("devices.txt", "a")
while True:
    newItem = input("Enter device name: ")
    if newItem == "exit":
        print("All done!")
        break
    file.write(newItem + "\n")
file.close()
