# 1.2.5.4: Create a While Loop
# Modify the While Loop to Use Break

x = input("Enter a number to count to: ")
x = int(x)
y = 1
while True:
    print(y)
    y = y + 1
    if y > x:
        break
