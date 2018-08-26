from .utils import *
from .search import *
from .manager import *
from .results import *
from .commands import *


# ----------------------------------------------------------------------------


global COMMAND_SEARCH
COMMAND_SEARCH = None


# ----------------------------------------------------------------------------


def install():
    """
    Add the cmd search functionality to Maya's native status bar.
    
    :raises RuntimeError: When the command search is already installed.
    """
    global COMMAND_SEARCH
    
    # validate timeline marker
    if COMMAND_SEARCH:
        raise RuntimeError("Command search is already installed!")

    # convert status line
    statusLine = getStatusLine()
    
    # get parent
    parent = mayaWindow()
    
    # get layout        
    layout = statusLine.layout()  

    # create command search
    COMMAND_SEARCH = SearchWidget(parent)
    layout.addWidget(COMMAND_SEARCH)
