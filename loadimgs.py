# -*- coding: utf-8 -*-
#tttt!python3
"""
Small script to import all of the AWS Photos into a single album in iOS Photos
"""

import os
import ui
import bz2
import photos
import console
from glob import glob
from base64 import b64decode


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
            

class CategoriesDataSource (object):
    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return 0

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.text_label.text = 'Foo Bar'
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        # If this is not implemented, no section headers will be shown.
        return 'Some Section'

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return True

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return True

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        pass

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        pass

    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        pass

    def tableview_did_deselect(self, tableview, section, row):
        # Called when a row was de-selected (in multiple selection mode).
        pass

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'


class ImagesDatasource (object):
    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return 0

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.text_label.text = 'Foo Bar'
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        # If this is not implemented, no section headers will be shown.
        return 'Some Section'

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return True

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return True

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        pass

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        pass

    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        pass

    def tableview_did_deselect(self, tableview, section, row):
        # Called when a row was de-selected (in multiple selection mode).
        pass

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'


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
        
        pyui = bz2.decompress(
            b64decode(self._load_ui())
        )
        self.content_view = ui.load_view_str(pyui.decode('utf-8'))
        self.content_view.background_color = '#333'
        self.content_view.frame = self.frame
        self.content_view.flex = 'WH'
        self.add_subview(self.content_view)
        
        # Setup the various connections
        self.main = self.content_view['main']
        self.label_image_num = self.main['image_num']
        self.preview_image = self.main['preview_image']
        self.preview_category = self.main['preview_category']
        self.list_set = self.main['list_set']
        self.list_view = self.main['list_view']
        self.label_category_preview = self.main['label_category_preview']
        self.label_image_preview = self.main['label_image_preview']
        
        # Default View
        self.preview_category.image = ui.Image('images/Database_AmazonElasticCache_Memcached.png')
        self.preview_image.image = ui.Image('images/Database_AmazonElasticCache_Redis.png')
        
        self.label_image_num.text = str(len(self.all_images))
        

        #self.demo_image_id = 0
        #ui.delay(self.preview_image_demo, 3)
        
    def _load_ui(self):
        ### UI - Used ui Packer by OMZ
        return '''\
QlpoOTFBWSZTWSir9ikABdPfgHVQUGd/9T/kHY6/79/+UAU73mdDygejZ6KA
sNKjT0mRtEMgZNMgMQ00Gg00GmQA0IZAIaEk0NANANBoD1AAAJEIpQP1I2UN
DT1AybQ9UZtUaaD0QyNAIlJNNTIaNNAAAAAAAAaAFSU0CNBpMp6iHqaZAGgx
ABhGJ6mmZLaTSYA0CRxgYL+P/YQEsrmhS7WgJaMKwFCWFDgMDrUtEXioRjjm
UDEioAGIqiaaqlvzpRCEhAtxaQoRaQSXFQCCVd1AbIJWoUzrNcx4dWrs65+o
sAZMzMyMKYD6xQlCUhYSXQqUImEi4JiO8dmj0Ggcy+WNuqPymygGEe41CLBb
gi+LqaFqSgXrHE9RiyJDWjEhfAMQOdVC4CIE6Bkz8IE6uFuC4UQMGDbd72kd
4BjRDSLWcDlhDtCV0F4FZlgL3uUUlVRIXYXaLpBkKg0PSbO7CNpkzAW1xKTA
KAgCBL0tKm7EBD0tsJGZmgIS1+qwSsgjM5TtIQTsPe8KwWhEBYdAMgaoB0T8
DJM1nATh6uy6zSR5w1wyS5w9HtM+eBAUAMiMiIR19PIQ0QoEoPpoh2mKy5G2
1SQSqgEZ4XaAKUYZ8H5JsZ4qdwbtHs0c6VARjVkK9wQMU6WzJSMmO2ODoDKW
Tie4yCHthwwYUA9ji6F9L4E6yklOFtyWzkAY2EnjcfIbbOewDamrpixEkYHh
YgQIuTdcRu98Z0iiv2xakIUG83jGzsTCUCokq5kKP2dLV6rWb7aJEwZmGeLi
AckSGNdXDMapvV6JKsyqJhsVpdY7UpngPKxxyji5nkGiWUoHNQM6uSMaRMVC
1RZ2FUTM4gw/hg5Zb7VrjmZYmNqpnrRVY63Vt4tZIHqcDyAbAm4b5UgDGmeL
aVlsKrLjxM/FLkiFdbqScN62bF/eCnKQOJrq7l1CHrCo8wy3ujUxet9OVrTn
HI8sq6wrN1kiso6ikQ2Jurawa7ZvktT4Atxf1gwX+chAGZAcQaPaJpaRHBoz
444gcf4NeW/lzG+vArl46rBAXf44Wl6bCroo+sXz1PA8kxm8OpuGAXyH+MyO
J2rMke5U+DjI0ose1HpeduLxW1UUIMcsSW0KK3moLVsLoljY/niyL1m6Qe+L
l6nYpr36XSqsiyKVPazuPX3yWR1vjly3poVeYZdkul665F6N33a6cOcWklyO
uR0uHGDjRG7pJM+9KijumyZcNyGYhqNPtf5hG5fvhcyGXqq8YrKivA2JmtmC
LJMpYjqsildqNDZiySw1xLd0dKKKxwxkHeOkuZ3Zf8s2malDOdJiyL0YlmkL
kpWSzai7JwTs4Q8LmnI34z33TOcyu7SatU1SWm+Q5F5tjii4ppM7WKml3bdI
ZNtVEcRlI0tUOhHN8xlg4nQ8NJpUVmYc0c8F5gbbGxG48EphqjB8ZWaNhnCz
sk2zTqjSG+cqDGrpUk2T5DONx8TCBAPZjAiyRiRhEl1Qv112sKhjjSWIGz5D
5D7BJ0mVoTp9KuvpsoiVD/4u5IpwoSBRV+xS'''


    def draw(self):
        #self.content_view.frame = self.frame
        pass
        
    
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
    v.present('sheet')
    #v.present('panel')

