# Import get_int
from cs50 import get_int

# Loop to guarantee the correct input
while True:
    height = get_int("What's the height of the pyramid? ")
    if 1 <= height <= 8:
        break

# Print the first pyramid
for row in range(height):
    for blank in range(height - row - 1):
        print(" ", end="")
    for column in range(row + 1):
        print("#", end="")

# Print the second pyramid
    print("  ", end="")
    for column in range(row + 1):
        print("#", end="")
    print("")
