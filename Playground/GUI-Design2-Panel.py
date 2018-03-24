# -*- coding: utf-8 -*-
"""
Markdown Editor - Preview Panel

This is being setup so that devices with less real estate
such as phones can use the panel (swipe right) when editing Markdown.

This will actually not be an editor at all, in fact it will
monitor the file that the user is editing for changes and 
auto refresh.

This allows the user to edit the markdown using the standard
pythonista editor, and swipe right for a preview.

It is intended to mimic the functionality of Editorial, which
is another tool by OMZ Software.

This doesn't really warrant using the WYSIWYG editor, but it
will definitely help illustrate how the application works.

Credits:
    GitHub CSS - https://github.com/sindresorhus/github-markdown-css
"""


import os
import re
import ui        # GUI Component
import editor    # Used to determine currently edited file
import markdown2 # Convert MD to HTML For preview
import markdown

class MarkdownPreview (ui.View):
    """
    MD Preview Class
    """
    
    def __init__(self, webview = None):
        # Using a static file until dev is done!
        self.markdown_file = os.path.join('..','README.md')
        self.markdown_html = self.markdown_data_get()
        self.name = os.path.basename(self.markdown_file)
        """
        Update polling:
            * Uses Pythonista's built-in update() timer
            * Disable by setting update_interval to 0
        """
        self.update_interval = 1
        
        self.webview = ui.WebView(
            #frame=(0, 0, w, (h-40)),
            flex='WB',
            scales_page_to_fit=True,
        )
        
        self.webview.load_html(
            self.render_template(self.markdown_html)
        )
        self.add_subview(self.webview)
    
    def draw(self):
        
        self.webview.frame = (0,0, self.width, self.height - 40)
    
    def markdown_data_get(self):
        """
        Method to grab the MD data
        """
        
        html_data = '<h1>No Markdown Found</h1>'
        try:
            html_data = markdown2.markdown_path(self.markdown_file)
        
        except FileNotFoundError:
            pass # TODO: Handle Not found exception
        except PermissionError:
            pass # TODO: handle perm exception
        
        return html_data
        
    def refresh_preview(self):
        if self.on_screen:
            #self.preview_webview.
            pass
    
    def update(self):
        """
        This is run every (self.update_interval)
        
        This will check for changes in the MD file
        """
        
        # Disabling until I write the code
        self.update_interval = 0
    
    def render_template(self, body):
        # For now - always use github style
        css = ''
        with open('assets/github-markdown.css', 'r') as f:
            css = f.read()
        
        template = ''
        with open('assets/template.html','r') as f:
            template = f.read()
        
        body_tag = re.compile(
            r'(\{\{(\s){0,}body(\s){0,}\}\})'
        )
        css_tag = re.compile(
            r'(\{\{(\s){0,}css(\s){0,}\}\})'
        )
        
        #template = css_tag.sub(template, css)
        #template = body_tag.sub(template, body)
        template = template.replace('{{ css }}', css)
        template = template.replace('{{ body }}', body)
        
        print(template)
        return template

window = MarkdownPreview()
window.present('panel')
