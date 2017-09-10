import os
import json

def get():
    """
    Get all pins from the global variable, if the global variable cannot be 
    found an empty dictionary will be returned.
    
    :return: Pins data
    :rtype: dict
    """
    if not "PINS" in globals().keys():
        return {} 
    return globals().get("PINS")
    
# ----------------------------------------------------------------------------  

def findLocation():
    """
    Pins get stored in the LOCALAPPDATA variable as a json file, since the
    local path changes per user, the path gets contructed each time. In case
    the LOCALAPPDATA directory gets cleared.
    
    :return: Path to pins json file
    :rtype: str
    """
    # get app data
    path = os.environ.get("LOCALAPPDATA")
    if not path:
        return
    
    # get app data file
    path = os.path.join(path, "rjCMDSearch.json")
    return path  
 
# ----------------------------------------------------------------------------  

def read(): 
    """
    Decode the data stored in the pins file and set it in the global PINS
    variable. If a path cannot be found, the PINS variable will be an empty
    dictionary.
    """
    global PINS
    PINS = {}

    # get pin path
    path = findLocation()
    if not path or not os.path.exists(path):
        return

    # read
    with open(path, "r") as f:
        info = f.read()

    if not info:
        return
        
    # decode data
    decoded = json.loads(info)
    if not decoded:
        return
    
    # update pins
    PINS.update(decoded)
          
def write():
    """
    Encode the data stored in the global PINS variable and write it to pins
    location path.
    
    :raises ValueError: if save location cannot be found
    """
    # get pin path
    path = findLocation()
    if not path:
        raise ValueError("Search Commands: file not found")
        return
    
    # write data
    data = json.dumps(get(), indent=4, separators=(",", ":"))
    with open(path, "w") as f:
        f.write(data)
        
    print "Search Commands: pins stored successfully ( {0} )".format(path) 