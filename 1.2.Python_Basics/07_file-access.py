# 1.2.6.1: Read an External File

devices = []
file = open("devices.txt", "r")
for item in file:
    item = item.strip()
    devices.append(item)
file.close()
print(devices)
