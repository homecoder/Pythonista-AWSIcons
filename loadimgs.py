# -*- coding: utf-8 -*-
#!python3
"""
Small script to import all of the AWS Photos into a single album in iOS Photos
"""

import os
import ui
import photos
import console


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
    """
    
    def __init__(self):
        self.flex = 'WH'
        self.background_color = '#fff'
        w, h = ui.get_window_size()
        self.frame = (0,0, w, h)
        title_text = 'AWS Image Export'
        title_font = ('<System>', 22)
        _, title_height = ui.measure_string(
                              title_text,
                              max_width=w,
                              font=title_font,
                              alignment=ui.ALIGN_CENTER,
                          )
        title_y = int(h * 0.15)
        title = ui.Label(
                    text=title_text,
                    name='title',
                    frame=(0, title_y, w, title_height),
                    font=title_font,
                    alignment=ui.ALIGN_CENTER,
                )
        
        pi_y = None # TBD - taking a break
        preview_image = ui.ImageView()
        preview_image.frame = (
            30,
            (),
            50,
            50,
        )
        
        preview_image.image = (
            ui.Image('images/AI_AmazonLex.png')
        )
        self.add_subview(preview_image)
        self.add_subview(title)
    


if __name__ == '__main__':
    """
    Main Application
    """
    awsie = AWSImageExporter()
    v = ExporterGUI()
    v.present('sheet')
    #t = awsie.albums[0]
    """
'add_assets', 'assets', 'can_add_assets', 'can_delete', 'can_remove_assets', 'can_rename', 'delete', 'end_date', 'local_id', 'remove_assets', 'start_date', 'subtype', 'title', 'type']    
    """

