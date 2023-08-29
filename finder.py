import os
import re
import csv
import glob

from builder import BUNDLE_NAME, BUNDLE_ENCODING, BUNDLE_TXT_DIR

CMD_REG = r"(\[STR.*\])\n(.*)"


def finder() -> None:
    txt_files = glob.glob(os.path.join(BUNDLE_TXT_DIR, "*.txt"))
    cache = []
    output = []

    if len(txt_files) == 0:
        print("Error: txt files not found. Create txt directory and put their into.")
        exit(1)

    if os.path.exists(BUNDLE_NAME):
        print("Error: Bundle already exists. Remove his before.")
        exit(1)

    for txt_file in txt_files:
        with open(txt_file, "r", encoding=BUNDLE_ENCODING) as fp:
            text_data = fp.read()
            lines = text_data[:-1].split("\n\n")
            for line in lines:
                if x := re.match(CMD_REG, line, re.DOTALL):
                    _, text = x.groups()
                    if not text in cache:
                        output.append([os.path.basename(txt_file), text, ""])
                        cache.append(text)
    with open(BUNDLE_NAME, 'w', newline='', encoding=BUNDLE_ENCODING) as fd:
        writer = csv.writer(fd)
        for row in output:
            writer.writerow(row)
    print("Bundle created.")


if __name__ == "__main__":
    finder()
