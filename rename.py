import os
import sys
from typing import *


def get_files(directory: str) -> List[str]:
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


# get arguments
args = sys.argv
if len(args) != 3:
    print("Usage: python main.py [csv file] [exibhit directory]")
    sys.exit(1)

# get csv file
csv_file = args[1]
if not os.path.exists(csv_file):
    print("Error: csv file does not exist")
    sys.exit(1)

# get exhibit directory
exhibit_dir = args[2]
if not os.path.exists(exhibit_dir):
    print("Error: exhibit directory does not exist")
    sys.exit(1)


files = get_files(f"{exhibit_dir}/access/ocr")

for file in files:
    print(file)
    os.system(f"mv \"{file}\" \"{file}.pdf\"")
#     if file.endswith("_ocred.pdf"):
#         os.system(f"mv \"{file}\" \"{file}\"")
