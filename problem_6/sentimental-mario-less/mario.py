# input must be 0 to 9
height = None
while True:
    try:
        height = int(input('Height: '))
    except ValueError:
        continue
    if (height > 0 and height < 9):
        break


i = 0
for i in range(height):
    for j in range(height - i - 1):
        print(' ', end="")

    for k in range(i + 1):
        print('#', end="")

    print()
