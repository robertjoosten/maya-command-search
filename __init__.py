"""			
Read all buttons in Maya's native menu and make them searchable and executable. 

.. figure:: https://github.com/robertjoosten/rjCMDSearch/raw/master/README.gif
   :align: center
   
`Link to Video <https://vimeo.com/109367578>`_

Installation
============
Copy the **rjCMDSearch** folder to your Maya scripts directory
::
    C:/Users/<USER>/Documents/maya/scripts
		
Usage
=====
Add the interface and functionality to Maya:
::
    import maya.cmds as cmds
    cmds.evalDeferred("import rjCMDSearch; rjCMDSearch.install()")

Note
====
Every time the UI is opened for the first time in a new session 
of Maya, the script loops over all of Mayas MenuBar content to 
retrieve all of the its information and store it in an easy accessible 
format. Since its over 1600 buttons, this process will take a few 
seconds. Its best to add this script to the userSetup.py so the 
interface will automatically be added to Maya when it is started.

The commands can always be refreshed by clicking on the magnifying
glass button.

The script now also tries to install a hotkey on the Ctrl + Alt + Space
combination. If there is already a hotkey on this combination the 
hotkey will not be installed. This hotkey will set the focus to the 
search command and open up the menu if there are any matches.

It is also possible to store your pins and create different pins sets 
for different tasks, meaning you can create your own custom menu. This 
functionality can be accessed by clicking the magnifying glass button.

Also a thank you too Perry Leijten and Guillaume Dufief for their 
ideas and pointers to improve the script.

Command Line
============
The following functions can be used outside of the ui. Make sure the 
language is set to python.
::
    import rjCMDSearch; rjCMDSearch.focus()  

Code
====
"""

from maya import cmds
from functools import wraps

from . import ui

__author__    = "Robert Joosten"
__version__   = "2.0.1"
__email__     = "rwm.joosten@gmail.com"
        
def install():
    """
    Add the cmd search functionality to Maya's native status bar. If 
    rjCMDSearch is already installed it will remove the previous instance.
    """
    # convert status line
    statusLine = ui.getStatusLine()
    
    # delete existing
    for child in statusLine.children():
        if child.objectName() == "CMDSearch":
            child.deleteLater()

    # add layout        
    layout = statusLine.layout()  

    # add to layout
    global CMD_SEARCH
    CMD_SEARCH = ui.SearchWidget(ui.mayaWindow())
    layout.addWidget(CMD_SEARCH)
    
    # register hotkey
    registerHotkey()
    
    print "Search Commands: installation succeeded ( UI )"
    
# ----------------------------------------------------------------------------

def registerHotkey():
    """
    Register hotkey to set focus to the search field, the hotkey combination
    registered is Ctrl + Alt + Space. If a hotkey is already registered to
    that combination a failed message will be printed.
    """
    hk = "rjCMDSearchHK"
    cmd = 'python("import {0}; {0}.focus()")'.format(__name__)
    registered = cmds.hotkey("Space", alt=1, ctl=1, query=1, name=1)
    
    # check if a hotkey is already registered to the key combination
    if registered and registered != hk:
        print "Search Commands: installation failed ( Hotkey )"
        return
    
    # register hotkey
    cmds.nameCommand(hk, annotation="Ctrl + Alt + Space", command=cmd)
    cmds.hotkey(k="Space", alt=1, ctl=1, name=hk)

    print "Search Commands: installation succeeded ( Hotkey )"
    
# ----------------------------------------------------------------------------

def getCMDSearch(func):
    """
    This decorator will only run the function if the cmd search can be 
    found, if this is not the case an error will be raised. The timeline 
    marker will be parsed as the first argument into the function provided.
    
    :raises ValueError: if cmd search cannot be found in globals
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not "CMD_SEARCH" in globals().keys():
            raise ValueError("CDM Search not installed!")
            
        cmdSearch = globals().get("CMD_SEARCH")
        return func(cmdSearch, *args, **kwargs)
    return wrapper
    
# ------------------------------------------------------------------------
  
@getCMDSearch  
def focus(cmdSearch):
    """
    Set focus to the input search field of the cmd search widget. Will
    return early if either the results window or the search bar already
    has focus.
    
    :param CMDSearch cmdSearch: decorator handles this argument
    """
    if cmdSearch.search.hasFocus() or cmdSearch.results.hasFocus():
        return

    ui.mayaWindow().activateWindow()
    cmdSearch.enter()
