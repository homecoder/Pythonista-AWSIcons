# -*- coding: utf-8 -*-
"""
I ended up importing the images into the same folder as the script I'd started.

This just moves all 'png' files into a folder called images.

Why I left it here: Example of using wildcards in python to move or copy files.
"""

import os
from glob import glob
from shutil import move

def move_images():
    current = os.getcwd()
    dest = os.path.join(current,'images')
    for image in glob(os.path.join(current,'*.png')):
        move(image, os.path.join(dest, os.path.basename(image)) )


move_images()
    
