# -*- coding: utf-8 -*-
"""
Design Notes:
    * Clean overall design
    * Ability to Pick whoch images/categories are to be exported
    * Uses title bar buttons for actions
"""

import ui
import os
from glob import glob

def set_layout_view_style(view):
    view_options = dict(
        background_color='#333333'
    )
    if isinstance(view, ui.View):
        for key, value in view_options.items():
            try:
                setattr(view, key, value)
            except AttributeError as e:
                pass

right_buttons = [
    ui.ButtonItem(
        title='Export Images',
        action=None
    )
]

left_buttons = [
    ui.ButtonItem(
        title='Reset',
        action=None
    )
]

# load sample images
source_glob = os.path.normpath(
    os.path.join('..','images','*.png')
)

sample_images = list(glob(source_glob))[0:19]
images_list = []
for image in sample_images:
    images_list.append({
        'image': ui.Image(image),
        'title': os.path.basename(image)
    })

list_data = ui.ListDataSource(images_list)

v = ui.load_view()

# Setup Layout View
set_layout_view_style(v)
v.right_button_items = right_buttons
v.left_button_items = left_buttons
v['main']['images'].data_source = list_data
v.present('sheet')
#v.present('panel')
