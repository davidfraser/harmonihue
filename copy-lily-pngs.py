import os
import shutil
import logging
from os.path import join, isdir
logging.getLogger().setLevel(logging.INFO)
out_lily = join('out', 'lily')

# Get all directories in out/lily
lily_dirs = [d for d in os.listdir(out_lily) if os.path.isdir(os.path.join(out_lily, d))]

# Process each directory
for directory in lily_dirs:
    # Get all PNG files in the current directory
    png_files = [
        os.path.join(out_lily, directory, f)
        for f in os.listdir(os.path.join(out_lily, directory))
        if f.endswith('.png')
    ]

    # Copy each PNG file to corresponding directory in out/
    for file_path in png_files:
        dest_path = file_path.replace(out_lily, 'out')
        logging.info(f"Copying {file_path} to {dest_path}")
        shutil.copy2(file_path, dest_path)