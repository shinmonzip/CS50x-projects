from cs50 import get_int

# Prompt the user for the pyramid's height
while True:
    height = get_int("Height: ")
    if 1 <= height <= 8:
        break  # Exit the loop if the input is valid

# Generate the half-pyramids
for i in range(1, height + 1):
    # Print the left pyramid with right alignment
    print(" " * (height - i) + "#" * i, end="")
    # Print the gap and the right pyramid
    print("  " + "#" * i)
