import csv
import os
import sys
from typing import *


def get_files(directory: str) -> List[str]:
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def process_file(filename: str, file_dir: str, language: str) -> None:
    print("\n\nProcessing file: " + filename)
    os.system(
        f"ocrmypdf --output-type pdf -l {language} \"{file_dir}/{filename}.pdf\" \"{file_dir}/{filename}.pdf\"")


def filter_dirs(dir: str) -> None:
    print("\nFiltering access directory...")
    dir = f"{dir}/access"
    os.system(f"mkdir \"{dir}_copy\" && mkdir \"{dir}_copy/non_ocr\" && mkdir \"{dir}_copy/ocr\" && cp -r \"{dir}\"/* \"{dir}_copy/non_ocr\" && cp -r \"{dir}\"/* \"{dir}_copy/ocr\" && rm -rf \"{dir}\" && mv \"{dir}_copy\" \"{dir}\"")


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

extracted_data: List[List[str]] = []
file_information: List[Dict[str, str]] = []

# read csv file
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    headers = next(reader, None) 

    filename_full_index = headers.index("Access Identifier")
    language_index = headers.index("language")
    for row in reader:
        filename_full = row[filename_full_index]
        language = row[language_index]

        # add to list
        extracted_data.append([filename_full, language])


# print(extracted_data)
# get all files in exhibit directory
filter_dirs(exhibit_dir)
files = get_files(f"{exhibit_dir}/access/ocr")

# loop through files
for file in files:
    # get filename
    filename_full = os.path.basename(file)
    filename = filename_full.split(".")[0]
    file_extension = filename_full.split(".")[1]

    # check if file is not a pdf
    if file_extension != "pdf":
        continue

    # get language
    language = None
    for item in extracted_data:
        if item[0] == filename:
            language = item[1] if item[1] != "" else "eng"
            # language = item[1]
            # add to list
            file_information.append(
                {
                    "filename": filename,
                    "language": language,
                    "base_dir": os.path.dirname(file)
                }
            )
            break

    # print results
    # print(f"{filename_full}: {language} \n{os.path.dirname(file)}")


# process files
for item in file_information:
    # print(item)
    process_file(item["filename"], item["base_dir"], item["language"])


