# rjCMDSearch
Read all buttons in Maya's native menu and make them searchable and executable. 

<p align="center"><img src="https://github.com/robertjoosten/rjCMDSearch/blob/master/README.gif"></p>
<a href="https://vimeo.com/109367578" target="_blank"><p align="center">Click for video</p></a>

## Installation
Copy the **rjCMDSearch** folder to your Maya scripts directory:
> C:\Users\<USER>\Documents\maya\scripts

## Usage
Add the interface and functionality to Maya:
```python
import maya.cmds as cmds
cmds.evalDeferred("import rjCMDSearch; rjCMDSearch.install()")
```
This line of code can also be added in the userSetup.py if you would like the functionality to persist.
  
## Note
Every time the UI is opened for the first time in a new session of Maya, the script loops over all of Mayas MenuBar content to retrieve all of the its information and store it in an easy accessible format. Since its over 1600 buttons, this process will take a few seconds. Its best to add this script to the userSetup.py so the interface will automatically be added to Maya when it is started.

The commands can always be refreshed by clicking on the magnifying glass button.

The script now also tries to install a hotkey on the Ctrl + Alt + Space combination. If there is already a hotkey on this combination the hotkey will not be installed. This hotkey will set the focus to the search command and open up the menu if there are any matches.

It is also possible to store your pins and create different pins sets for different tasks, meaning you can create your own custom menu. This functionality can be accessed by clicking the magnifying glass button.

Also a thank you too Perry Leijten and Guillaume Dufief for their ideas and pointers to improve the script.

## Command line
The following functions can be used outside of the ui. Make sure the 
language is set to python.

```python
import rjCMDSearch; rjCMDSearch.focus()
```    
