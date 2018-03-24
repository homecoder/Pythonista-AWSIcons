# Pythonista-AWSIcons

This isn't extremely useful for Pythonista users; however it will service as an example of using some of the photos library functionality.

Note: This will *only* work with Pythonista.

## What it does it do?

A class which provides the following examples:
* List albums
* Create a new album (checks for existing album)
* Add image to album
* Add bulk images to album
    * This adds the images individually so that I can give a progress update using Pythonista's ui
    * Images can either be a Pythonista Asset or a file
    * Checks for file existence
* Abundance of exception handling
* Commented
    * Sphinx comments will be done later, I've been changing my mind a lot on this

## GUI Component

I've taken the opportunity to put a bit more effort into this to help me with teaching a couple of people Pythonista.

I am developing two separate GUI components, one using strictly code, and one using the WYSIWYG editor which comes with Pythonista.

## Why do it? Why on github?

Good Question - I did this because I am using the mobile app [Flowdia Diagrams](https://itunes.apple.com/us/app/flowdia-diagrams/id1170864140?mt=8). It doesn't (to my knowledge) 

I've uploaded it to github in order to share.

In addition, I am using this as an example of my Python development skills for a few job opportunies that I have in front of me.

## Application Future

Since I I decided to get a little over zealous when developing this, I am planning on sharing this prior to full completion.

I am doing this because I plan to transform this app into something a little more useful / generic as I'd rather use this as a tool for others to learn from instead of just a tool to save images to my library (which was the initial intent).

## TODO

With the above statement, this is what I plan to do:

* Setup the Image saving as a "wrench" tool in Pythonista
* Split the code out into separate components
* Build out a series of README files in the form of lessons
* Comment the application using Sphinx style comments
* Add the ability to download the icon assets for AWS, Azure, and GCP
* Add the ability to select which icons you wish to export
* Add the ability to check for icons already exported
* Add remove/delete from the Icon albums
* Add a configuration section with options
* Continue adding to the application to showcase multiple Pythonista modules:
	* ui (currently in-use)
	* photos (currently in-use)
	* Wrench tool (I need to figure out what this is actually named)
	* appex (Ability to "Open With" and allow users to use icons downloaded from their browser to import into the app to be managed)
	* console (currently in-use)
	* dialogs (coming soon)
	* clipboard (snag URLs to icons from clipboard)

## TODO Tool

I was also inspired when writing this app to setup a TODO tool.

The TODO tool will be a wrench application which uses the "editor" pythonista module to parse the existing open file, or all python files in the current project and add them to the README file.

This would work by:

* Specify the README tool for the current app (configuration item)
* Specify which file(s) are to be scanned
* Search for "^# TODO: (.*)$" (regex) and set them up as a list
* Specify which section of the README file needs to be filled in, OR use a README template, unsure yet which, or possibly both

In the end the developer could pull all TODOs out and specify them in the README file.

💡 Ideas:

* Add functionality to create issues in GitHub for todos
* Add YAML capabilities for config
* Create a better Markdown editor for the wrench menu, essentially creating a full README utility rather than just TODOs

