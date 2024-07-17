import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
                    "uploads/empty.txt",
                    "app.py",
                    "requirements.txt",
                    "static/style.css",
                    "templates/index.html",
                    "templates/convert.html",
                    "templates/edit.html",
                    "templates/remove.html",
                ]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        if filename != "":
            with open(filepath, 'w') as f:
                pass
                logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} file is already available")