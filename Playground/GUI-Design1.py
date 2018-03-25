# -*- coding: utf-8 -*-
"""
Design Notes:
    * Clean overall design
    * Ability to Pick whoch images/categories are to be exported
    * Uses title bar buttons for actions

TODO:
    * Implement Categories for this design(1)
    * 
"""

import ui
import os
from glob import glob


### UI
data = '''\
QlpoOTFBWSZTWWkn3vgABdTfgHVQUGd/9T/kHY6/79/+UAU7xNDlmTRcDQGD
RNTBNoRk0pPUAAHqaNAD1AAGg0JponqFA/QoDRoNANAAAAAJERqimPUYUAPU
aPUZqYmnlGg0xMmjQHNGTEwATEYEaYEGIwTJgEYFSRAjQmCIh6mgAAAZBo00
yeppiS3U0mANAkcQGC/j/2EBLLc0KXe8BLRjWIoS4ocBiLRF0pIpUhjjmkGd
SQDOSRHfJJGXntaFKpRlUlqWVJakVskgUi/msTOkYyFu7P33l4I7Hfunt5xY
AyZmZkYWYD7RQlCUhcSXTYY4RMJFAmI3Duz+gzjmX8IwtY7E2WAYDOceIdHX
x5Oi39WnFS/M+RjbUUw8WjDgA8gi0TcEQLfDTwagJ4dTcFBYgYMG26q8jqAY
0Q0i93A5YQ7wlQFQi7VwKqizdgLWkKYU0UkGwVgyvQdG3CNxkzAX1xKTALAQ
BAl6WqYaG3iGEYpbkIaQQlr37hK2AIxwQ8ZgJeqqGkGrIgLRlBkDZAMr78kc
2eIePTjhbKpFONNCSVZAqLJzyRICsAyIyIhOnPokM9CuqH8dtDvMW2crbask
Eq0AjNCxgFlGGbB+NGizMkwDTXJ74aSXBkneiyEWFpoCBifqfYnEZPOu00aN
I6IWSGQYeLoLmHAHg4I2mtLjNYxZLmnuTpogEjkKlGA8hddJYoUqG0HFpFOG
60KSqAYi08GpPNVZ12TRlvpaquK8HiKXwo4SsMiPZnELFvhVcrNY6z1ZAwZm
H5CgaEZAha90GguzdcmMiuZKMw8WWVHQ2lLSwyKZwrC1DOofAqxGbQNFRjoS
JQ1WSzmFZGR4xlt25lxYS8lYwxUFS2Y8jBuskPa3jIkgA+ooBxA2BP3xWTQY
10tPVY7BXR5cuJsjzQDkn1IoMLN9qfAFnGIOBuunC4Yd2qOcVxRj5WotNeD5
55wqdardq5pNkHRhcSgH2zRZzD6P0yi5T2BbinsBgulGEDaDnBo4RNLQI1Z8
3Jye8Dk6zi06+Y0reXuKj83LGVfpjeYRsLRY+cYT+njfTMpvg7jdDEMJD0tC
Ow7180etU9rska0XPUj+X4bjAxl7SFJradUVnC0k4S5bHM1RpM54fvD0G+Qe
yLMFOanLxUtKq6LopR6mi09HiJdHTCOfLfJqVgY59JaYN17oxRf6+PDpFklk
d2R1tDhBwojXqGnaVFTwmwnzUEMEB2CZ/CLpIwYjvqBGpGdEaoyDbk8huTr1
JSplLkdy6KV3o1NmaWhxxL+EdaKituOUg7TqWaWz/5dtNJSpNJ1mTMwRkXaw
tJUrNdtRbOcE5cIeRfonI33nss0nQrw1nFxTikvN8hyMDbHYixU1ml7ymmt+
+0howqojshmS2sOpHxGWHA6HkqRkYc0c8JhNx23NiNx45THijGe7K0RsmkLu
cm2a9yNYb0Ma5SpJse8aRuemvWKB1ppg0m2mhpjQ9pIMt72/aQcfHZLjA6Pm
PlPuEnUbLwnZ9SpfaU4UP/i7kinChINJPvfA
'''
import ui
import bz2
from base64 import b64decode
pyui = bz2.decompress(b64decode(data))
v = ui.load_view_str(pyui.decode('utf-8'))
### UI

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


def toggle_checkmark(sender=None):
    """
    Need to rework this. I broke it.
    """
    accessories = ['checkmark', '']
    if sender:
        item = sender.items[sender.selected_row]
        item_at = sender.items[sender.selected_row]['accessory_type']
        item_id = accessories.index(item_at)
        item_at = accessories[int(not item_id)]
        sender.items[sender.selected_row]['accessory_type'] =  item_at
        sender.tableview.reload()

def export_items(sender=None):
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
        'title': os.path.basename(image),
        'accessory_type': 'checkmark',
    })

tv_delegate_options = dict(
    action=toggle_checkmark,
    delete_enabled=False,
    font=('<System>', 15),
    highlight_color=(1.0,1.0,1.0,0.0), # Transparent
    move_enabled=False,
    number_of_lines=2,
)
list_data = ui.ListDataSource(images_list)
for key, value in tv_delegate_options.items():
    try:
        setattr(list_data, key, value)
    except:
        pass

#v = ui.load_view()

# Setup Layout View
set_layout_view_style(v)
v.right_button_items = right_buttons
v.left_button_items = left_buttons
v['main']['images'].data_source = list_data
v['main']['images'].delegate = list_data
v.present('sheet')
#v.present('panel')
