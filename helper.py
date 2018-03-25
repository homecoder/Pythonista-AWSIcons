# -*- coding: utf-8 -*-
"""
I ended up importing the images into the same folder as the script I'd started.

This just moves all 'png' files into a folder called images.

Why I left it here: Example of using wildcards in python to move or copy files.
"""

import os
from glob import glob
from shutil import move
from loadimgs import AWSImageExporter, ExporterGUI
import photos

def move_images():
    current = os.getcwd()
    dest = os.path.join(current,'images')
    for image in glob(os.path.join(current,'*.png')):
        move(image, os.path.join(dest, os.path.basename(image)) )

def export_images():
    all_images = glob(os.path.join(
        'images',
        '*.png',
    ))
    
    album = photos.create_album('AWS Icon Export')
    album_assets = []
    for image in all_images:
        print('Processing Image: {}'.format(os.path.basename(image)))
        img_asset = photos.create_image_asset(image)
        album_assets.append(img_asset)
    
    print('Exporitng...')
    album.add_assets(album_assets)
    
    
export_images()
#move_images()
    
