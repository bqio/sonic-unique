import os
import csv
import shutil

BUNDLE_NAME = "bundle.csv"
BUNDLE_ENCODING = "utf-8-sig"
BUNDLE_TXT_DIR = "txt"
BUNDLE_BUILD_DIR = "build"
BUNDLE_MAX_COLS = 3


def bundle_is_valid() -> bool:
    with open(BUNDLE_NAME, "r", encoding=BUNDLE_ENCODING) as fp:
        csv_reader = csv.reader(fp)
        for row in csv_reader:
            if len(row) != BUNDLE_MAX_COLS:
                return False
    return True


def builder() -> None:
    if not os.path.exists(BUNDLE_NAME):
        print(f"Error: {BUNDLE_NAME} not found. Use finder.py")
        exit(1)

    if not bundle_is_valid():
        print("Error: Invalid bundle syntax.")
        exit(1)

    print("Building...")
    if not os.path.exists(BUNDLE_BUILD_DIR):
        os.mkdir(BUNDLE_BUILD_DIR)
    shutil.rmtree(BUNDLE_BUILD_DIR)
    shutil.copytree(BUNDLE_TXT_DIR, BUNDLE_BUILD_DIR)
    files = os.listdir(BUNDLE_BUILD_DIR)

    for file_name in files:
        file_path = os.path.join(BUNDLE_BUILD_DIR, file_name)
        file_data = None
        with open(file_path, "r", encoding=BUNDLE_ENCODING) as fp:
            file_data = fp.read()
        with open(BUNDLE_NAME, "r", encoding=BUNDLE_ENCODING) as fb:
            csv_reader = csv.reader(fb)
            for row in csv_reader:
                file, en, ru = row
                if ru != "":
                    print(f"{file_name}: Patching '{en}' to '{ru}'")
                    file_data = file_data.replace(en, ru)
        with open(file_path, "w", encoding=BUNDLE_ENCODING) as fd:
            fd.write(file_data)
    print("Done.")


if __name__ == "__main__":
    builder()
