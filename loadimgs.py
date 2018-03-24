# -*- coding: utf-8 -*-
#tttt!python3
"""
Small script to import all of the AWS Photos into a single album in iOS Photos
"""

import os
import ui
import photos
import console
from glob import glob


class AWSImageExporter (object):
    
    
    def __init__(self, source_path=None):
        
        if not source_path:
            source_path = os.getcwd()
        
        if not os.path.exists(source_path):
            raise FileNotFoundError('Invalid path')
        
        # Setup Class Properties
        self.albums = []
        self.album_titles = []
        self.smart_albums = []
        self.smart_album_titles = []
        self.image_path = os.path.join(os.getcwd(),'images')
        self.errors = [] # used for batch operations
        
                
    def _alert_error(self, message):
        return console.alert('Error', message, 'Ok', hide_cancel_button=True)
    
    def _alert_warning(self, message):
        return console.alert('Warning', message, 'Ok', hide_cancel_button=True)
        
        
    def album_create(self, title):
        title = title.strip()
        
        if title in self.album_titles:
            self._alert_error('Album already exists.')
            return
            
        try:
            album = photos.create_album(title)
            if isinstance(album, photos.AssetCollection):
                self.albums.append(album)
                self.album_titles.append(title)
                return album
            else:
                self.albums_load()
                if title in self.album_titles:
                    id = self.album_titles.index(title)
                    return self.albums[id]
                else:
                    self._alert_error('An unknown error has occurred resulting in the album not being created.\n' \
                                      'Please restart Pythonista and try again.')
                    return False
            
        except Exception as e:
            """
            There are no documented expected Exceptions with this call; so our only choice is a generic handler.
            Note: This is working primarily around iOS's internal frameowrks. Determing the exception time, or rather
                  any exception beyond a base exception (captured above).
            """
            self._alert_error('Unable to create album {}. \nError: {}'.format(title, e))

                
    def albums_load(self, load_smart_albums=False):
        # Get Album Titles
        albums = photos.get_albums()
        for album in albums:
            self.albums.append(album)
            self.album_titles.append(album.title)        
        
        return # Although not required, I am a fan of returning all methods
                        
    def image_to_asset(self, image, batch=False):
        """
        Convert image (file) to Pythonista Image Asset        
        """
        
        # Check if it's already an asset
        if isinstance(image, photos.Asset):
            return image
        
        # It's not already an asset, lets convert it.
        try:
            return photos.create_image_asset(image)
        except FileNotFoundError:
            if batch:
                self.errors.append('Error: File {} not found.'.format(image))
            else:
                self._alert_error('File Not Found')
        except PermissionError:
            if batch:
                self.errors.append('Unable to access image {}, Access is Denied. \n' \
                                   'If issue persists restart Pythonista.'.format(image))
            else:            
                self._alert_error('Unable to access image, Access is Denied. If issue persists restart Pythonista.')
        except Exception as e:
            raise e
            
        return False
    
    def album_add_image(self, album, image, batch=False):
        """
        Add an Image to an Album
        """
        if not isinstance(album, photos.AssetCollection):
            raise TypeError('Invalid Album. Must be Pythonista AssetCollection')
        
        if not album.can_add_assets():
            if batch:
                self.errors.append('You can\'t add images to the album {}'.format(album.title))
            else:
                self._alert_error('You can\'t add images to the album {}'.format(album.title))
            return False
        
        if isinstance(image, (list, tuple,)):
            """
            Technically allowed, but I dont want to.
            This is NOT pythonic is any way - don't do this
            I am doing it because I am testing something...
            """
            raise PermissionError('I am not giving you permission to use lists/tuples.')
            pass
        
        if not isinstance(image, photos.Asset):
            image = self.image_to_asset(image)
        try:
            return album.add_assets([image])
        except Exception as e:
            """
            There are no documented expected Exceptions with this call; so our only choice is a generic handler.
            Note: This is working primarily around iOS's internal frameowrks. Determing the exception time, or rather
                  any exception beyond a base exception (captured above).
            """
            self._alert_error('Unable to add assets to album {}. \nError: {}'.format(album.title, e))
            if batch:
                # Stop execution on batch run.
                raise e
        return False
    
    def album_add_batch_images(self, album, images):
        """
        Add a batch of images to an iOS album. This is the primary intent of the app.
        """
        if not isinstance(album, photos.AssetCollection):
            raise TypeError('Invalid Album. Must be Pythonista AssetCollection')
        
        # Ensure all images are assets
        images_to_add = []        
        for image in images:
            images_to_add.append(self.image_to_asset(image, batch=True))
        
        # Add all of those images to the album
        total_images = len(images_to_add)
        count = 0
        for image in images_to_add:
            self.album_add_image(albun, image, batch=True)
            count += 1
            

class ExporterGUI (ui.View):
    """
    UI and Implementation of AWSImageExporter
    
    This utilizes the built-in GUI components native to iOS.
    The commands used below are wrappers available in the
    Pythonista Library.
    
    There is also the option of using a WYSIWYG style editor,
    but that seems so much less fun.
    """
    
    def __init__(self):
        
        self.animate_demo = True
        self.flex = 'WH'
        self.name = 'AWS Image Export'
        self.background_color = '#fff'
        w, h = ui.get_window_size()
        self.frame = (0,0, w, h)
        buffer = 20
        
        # Setup Exporter
        
        self.exporter = AWSImageExporter()
        
        # Setup images
        self.image_list = {}
        self.all_images = [] 
        
        # Setup Categories
        self.categories = []
        
        # Grab Images into above vars
        self.load_images()
        
        # Remove duplicates in categories, and sort
        self.categories = sorted(list(set(self.categories)))
        
        
        title_text = 'AWS Image Export'
        title_font = ('<System>', 22)
        _, title_height = ui.measure_string(
                              title_text,
                              max_width=w,
                              font=title_font,
                              alignment=ui.ALIGN_CENTER)
        title_y = int(h * 0.06)
        title = ui.Label(
                    text=title_text,
                    name='title',
                    frame=(0, title_y, w, title_height),
                    font=title_font,
                    alignment=ui.ALIGN_CENTER,
                    flex='WB'
                )
        
        # Preview Image
        pi_y = (title_y+title_height+buffer)
        pi_x = (w / 2) - 45
        self.preview_image = ui.ImageView(flex='LBR')
        self.preview_image.frame = (
            pi_x,
            pi_y,
            75,
            75,
        )
        
        self.preview_image.image = (
            ui.Image('images/Database_AmazonElasticCache_Memcached.png')
        )
        
        self.demo_image_id = 0
        
        ui.delay(self.preview_image_demo, 3)
        
        # Status Label
        
        sl_y = (pi_y+75+buffer)
        self.status_label_text = '{} Images to Export'.format(len(self.all_images))
        _, sl_h = ui.measure_string(
            self.status_label_text,
            max_width=w,
            font=title_font,
            alignment=ui.ALIGN_CENTER)
        
        status_label = ui.Label(
            text=self.status_label_text,
            frame=(0, sl_y, w, sl_h),
            alignment=ui.ALIGN_CENTER,
            flex='WB'
        )
        
        # Now - instead of whatever I was thinking before..
        
        # Setup Select Category Button
        self.sc_button = ui.Button(
            name='sc_button',
            title='Select Categories',
            action=None # TODO: Set Action
        )
        
        # TODO: Reset Categories Button
        
        # TODO: Start Export Button
        
        
        
        self.add_subview(self.preview_image)
        self.add_subview(title)
        self.add_subview(status_label)
    
    def preview_image_demo(self, sender=None):
        """
        Animate the preview image..
        I've selected between memcached and redis, as it is..
        
        My initials - M, R.
        """
        preview_images = [
            ui.Image('images/Database_AmazonElasticCache_Memcached.png'),
            ui.Image('images/Database_AmazonElasticCache_Redis.png'),
        ]
        
        # Switch between 1 and 0
        self.demo_image_id = int(not self.demo_image_id)
        # Could also do: abs(self.demo_image_id + -1)
        # I ❤️ Math, so logical, and in this case, so finite
        
        self.preview_image.image = preview_images[
            self.demo_image_id
        ]
        if self.animate_demo:
            ui.delay(self.preview_image_demo, 3)
        
        return 
    
    def load_images(self):
        """
        Load all .png images from the images folder
        """
        images = glob(
            os.path.join(
                os.getcwd(), 
                'images', 
                '*.png'
            )
        )
        
        for image in images:
            self.all_images.append(str(image))
            c = str(image).split('_')
            category = c[0]
            self.categories.append(category)
            if category not in self.image_list.keys():
                self.image_list[category] = []
            
            self.image_list[category].append(str(image))
        return 
    
    def will_close(self):
        # Disable the demo run - else it will keep going after closing the window
        self.animate_demo = False
        return 


if __name__ == '__main__':
    """
    Main Application
    """
    awsie = AWSImageExporter()
    v = ExporterGUI()
    #v.present('sheet')
    v.present('panel')

