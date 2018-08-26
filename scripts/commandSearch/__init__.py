"""			
Read all buttons in Maya's native menu and make them searchable and executable. 

.. figure:: /_images/commandSearchExample.gif
   :align: center
   
`Link to Video <https://vimeo.com/109367578>`_

Installation
============
* Extract the content of the .rar file anywhere on disk.
* Drag the commandSearch.mel file in Maya to permanently install the script.

Note
====
Every time the UI is opened for the first time in a new session 
of Maya, the script loops over all of Mayas MenuBar content to 
retrieve all of the its information and store it in an easy accessible 
format. Since its over 1600 buttons, this process will take a few 
seconds.

The commands can always be refreshed by clicking on the magnifying
glass button.

It is also possible to store your pins and create different pins sets 
for different tasks, meaning you can create your own custom menu. This 
functionality can be accessed by clicking the magnifying glass button.

Also a thank you too Perry Leijten and Guillaume Dufief for their 
ideas and pointers to improve the script.

Hotkey
======
The hotkey function can be used to manage the command search widget. 
This command will set focus to the widget.

::
    import commandSearch; commandSearch.focus()  
"""
from .ui import install
from .hotkey import *

__author__    = "Robert Joosten"
__version__   = "2.0.2"
__email__     = "rwm.joosten@gmail.com"
