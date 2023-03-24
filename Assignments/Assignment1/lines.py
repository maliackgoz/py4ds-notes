import argparse
import sys

# Create command-line argument parser
parser = argparse.ArgumentParser()

# Add positional argument
parser.add_argument('file')

# Parse arguments from terminal
args = parser.parse_args()

# Access the arguments
file = args.file

lineCount = 0

# Check for errors and exit if necessary
if not file.endswith('.py'):
    sys.exit("Error: File must end in .py")
try:
    with open(file, "r") as my_file:
        pass
except FileNotFoundError:
    sys.exit("Error: File does not exist")

with open(file, "r") as my_file:
    lines = my_file.readlines()
    for i in lines:
        if not i.startswith("#") and not i.isspace():
            lineCount += 1

# print the final line count
print(lineCount)