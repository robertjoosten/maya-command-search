import re
from maya import cmds

from .ui import utils

def get():
    """
    Get all registered commands from the global variable, if the global 
    variable cannot be found an empty dictionary will be returned.
    
    :return: Commands data
    :rtype: dict
    """
    if not "COMMANDS" in globals().keys():
        return {} 
    return globals().get("COMMANDS")
    
# ----------------------------------------------------------------------------

def filter(search):
    """
    The search string is processed find matches within the commands variable.
    
    :param str search: search string to match with commands
    :return: Matching commands
    :rtype: list
    """
    matches = []
    regexes = []
    
    # generate regex
    if search:
        for p in search.split():
            regexes.append(
                re.compile(
                    r'.*' + 
                    re.sub( r'\W', '.*', p.strip() ) + 
                    r'.*'
                )    
            )

    # filter commands
    for k, v in COMMANDS.iteritems():
        if v.get("pin"):
            matches.append(v)
            continue
            
        states = []
        for regex in regexes:
            states.append( 
                re.match(
                    regex.pattern, 
                    v.get("search"), 
                    re.I
                )
            )
            
        if regexes and None not in states:
            matches.append(v)

    matches.sort(key=lambda x:(-x["pin"], x["hierarchy"]))
    return matches

# ----------------------------------------------------------------------------  

def store():  
    """
    Process Maya's menubar to see if any if its children meet the search 
    command requirements. If so, the button and commands will be added 
    to the commands variable.
    """
    # reset commands
    global COMMANDS
    COMMANDS = {}
    
    # loop menu bar
    menuBar = utils.mayaMenu()
    _store(menuBar)
    
    print "Search Commands: {0} buttons registered".format(len(COMMANDS))

def _store(parent, parents=[]):
    """
    Process the parent to see if any if its children meet the search 
    command requirements. If so, the button and commands will be added 
    to the commands variable.
    
    :param QWidget parent: direct parent
    :param list parents: linked menu's
    """
    children = parent.children()
    for i, item in enumerate(children):
        # tree
        tree = parents[:]
    
        # get items
        name = item.objectName().encode("utf-8")
        
        # skip if no item name
        if not name:
            continue
            
        # process menu
        if type(item) == utils.QMenu:
            tree.append(
                getMenu(item)
            )
            
        # process item
        elif type(item) == utils.QWidgetAction:  
            # get dynamic p
            dynamic = item.dynamicPropertyNames()
            
            if not "isOptionBox" in dynamic:
                # main item
                getItem(item, name, tree)
            else:
                # option box item
                getItemOptionBox(item, parent)
            
        # store as parent
        parent = name   
        
        # process next
        _store(item, tree)
        
# ----------------------------------------------------------------------------  
          
def getMenu(menu):
    """
    Get the name of the QMenu parsed.
    
    :param QMenu menu:
    :return: Menu name
    :rtype: str
    """
    name = menu.title().encode("utf-8")
    menu.aboutToShow.emit()
    return name
    
# ----------------------------------------------------------------------------
    
def getItem(item, name, parents):
    """
    Get data from item and store it into COMMANDS variable.
    
    :param QWidgetAction item:
    :param str name: 
    :param list parents: List f all parents, used for hierarchy
    """

    # get name
    text = item.text().encode("utf-8")
    if not name or item.isSeparator() or item.menu():  
        return
    
    # add last parent
    parents.append(text)
        
    # get icon
    icon = cmds.menuItem(utils.qtToMaya(item), query=True, image=True)
      
    # store commands      
    COMMANDS[name] = dict( )
    COMMANDS[name]["name"] = text
    COMMANDS[name]["pin"] = False
    COMMANDS[name]["cmd"] = item 
    COMMANDS[name]["icon"] = utils.QIcon( ":/{0}".format(icon))
    COMMANDS[name]["group"] = parents[0]
    COMMANDS[name]["search"] = "".join([p.lower() for p in parents]) 
    COMMANDS[name]["hierarchy"] = " > ".join(parents)
      
def getItemOptionBox(item, name):
    """
    Get data from option item and store it into COMMANDS variable.
    
    :param QWidgetAction item:
    :param str name: 
    """
    if not name in COMMANDS.keys():
        return

    COMMANDS[name]["cmdOption"]   = item
