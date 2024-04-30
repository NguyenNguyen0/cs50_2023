from cs50 import get_float

# input from user
owed = None
while True:
    try:
        owed = get_float('Change owed: ')
    except ValueError:
        continue

    if (owed > 0):
        break

# make float point to in int: 0.23 to 23
owed = owed * 100

# caculate quaters, dimes, nickel, pennies
def quaters_count():
    global owed
    if owed >= 25:
        quaters = int(owed / 25)
        owed -= quaters * 25
        return quaters
    return 0

def dimes_count():
    global owed
    if owed >= 10:
        dimes = int(owed / 10)
        owed -= dimes * 10
        return dimes
    return 0

def nickels_count():
    global owed
    if owed >= 5:
        nickels = int(owed / 5)
        owed -= nickels * 5
        return nickels
    return 0

def pennies_count():
    global owed
    if owed >= 1:
        pennies = owed
        owed = 0
        return pennies
    return 0

# caculate and print total coins
total = quaters_count() + dimes_count() + nickels_count() + pennies_count()
print(int(total))