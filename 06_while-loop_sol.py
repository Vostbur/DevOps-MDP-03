# 1.2.5.5: Use a While Loop to Check for User Quit Command

while True:
    x = input("Enter a number to count to: ")
    if x == 'q' or x == 'quit':
        break

    x = int(x)
    y = 1
    while True:
        print(y)
        y = y + 1
        if y > x:
            break
