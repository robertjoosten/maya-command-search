from functools import wraps
from . import ui


def getCommandSearch(func):
    """
    This decorator will only run the function if the command search can be 
    found, if this is not the case an error will be raised. The timeline 
    marker will be parsed as the first argument into the function provided.
    
    :raises ValueError: if command search doesn't exist
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get timeline marker
        commandSearch = ui.COMMAND_SEARCH
        
        # validate timeline marker
        if not commandSearch:
            raise ValueError("Command search not installed!")
            
        # run function
        return func(commandSearch, *args, **kwargs)
    return wrapper
