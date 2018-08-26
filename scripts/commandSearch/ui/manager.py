from . import utils
from .. import commands, pins

class ManagerMenu(utils.QMenu):
    """
    Manager Menu 
    
    Used to create / edit and delete different pin sets and be able to switch 
    between them, it also features the functionality to refresh the command 
    list.
    
    :param QWidget parent:
    """
    def __init__(self, parent=None):
        utils.QMenu.__init__(self, parent)
        
        # variable
        self.parent = parent
        self.active = None
        
        # menu
        self.setObjectName("PinMenu")
        self.setMinimumWidth(140)
        
        # connect
        self.aboutToShow.connect(self.aboutToShow_)
        
    # ------------------------------------------------------------------------
                
    def aboutToShow_(self):
        """
        Before the menu is shown, the pin set are read, the menu is populated 
        with the read pin set data and the menu is positioned.
        """
        # get pins
        pins.read()
        
        # populate
        self.populate()
        self.position()
        
    # ------------------------------------------------------------------------
    
    def add(self, widget):
        """
        Add widget to a QWidgetAction and add it to the menu.
        
        :param QWidget widget: widget to be added to the menu
        """
        action = utils.QWidgetAction(self)
        action.setDefaultWidget(widget)
        self.addAction(action)
        
    # ------------------------------------------------------------------------

    def populate(self):
        """
        Populate the menu, clears the menu first, then adds the pins, set 
        manager and finally the command refresh option.
        """
        # clear menu
        self.clear()
        
        # pins
        self.populatePins()
        self.populateSets()
        self.populateCommands()
  
    # ------------------------------------------------------------------------
    
    def populatePins(self):
        """
        Read pin set data and create radio buttons so the user can switch
        between the different sets available.
        """ 
        # get pin names
        names = pins.get().keys()
        if not names:
            return
            
        # add pins group
        self.group = utils.QButtonGroup(self)
        self.group.buttonReleased.connect(self.setActive)
        
        g = utils.Divider(self, "Pins")
        self.add(g)
        
        # add pins
        for name in names:
            # create pin
            radio = utils.QRadioButton(name)
            
            # set active
            if name == self.active:
                radio.setChecked(True)
            
            # add pin
            self.add(radio)
            self.group.addButton(radio)
                
    def populateSets(self):
        """
        Create set manager buttons.
        """ 
        g = utils.Divider(self, "Sets")  
        self.add(g)        
        
        self.edit = utils.QLineEdit()
        self.add(self.edit)    

        self.addAction("Add / Edit", self.pinAdd)
        self.addAction("Clear", self.pinClear)
        self.addAction("Delete", self.pinDelete)
        
    def populateCommands(self):
        """
        Create command refresh button.
        """ 
        g = utils.Divider(self, "Commands")  
        
        self.add(g)
        self.addAction("Refresh", self.refresh)
        
    # ------------------------------------------------------------------------
                
    def position(self):
        """
        Position the menu underneath its parent.
        """
        pos = self.parent.parentWidget().mapToGlobal(self.parent.pos())
        posX = pos.x()
        posY = pos.y()
        height = self.parent.height()
        
        posY += height
        self.move(posX + 8, posY) 
        
    # ------------------------------------------------------------------------
        
    def setActive(self):
        """
        Switch active pin set to checked radio button.
        """
        # set active
        self.active = self.group.checkedButton().text()
        
        # get pins
        pinned = pins.get().get(self.active) or []
        for k, v in commands.get().iteritems():
            if v.get("hierarchy") in pinned:           
                v["pin"] = True
            else:                                             
                v["pin"] = False
                
    # --------------------------------------------------------------------
    
    @property    
    def pinName(self):
        """
        Get text from QLineEdit
        """
        return self.edit.text().lower()
        
    def pinAdd(self):
        """
        Add pin set, store all if the currently pinned commands and store
        then under the provided pin set name.
        
        :raises ValueError: if name is invalid or no pins are found
        """
        # get pin name
        if not self.pinName:
            raise ValueError("Search Commands: invalid name")
            return
        
        # get pinned name
        pinned = []
        for k, v in commands.get().iteritems():
            if not v.get("pin"):
                continue
                
            pinned.append(v.get("hierarchy"))
        
        if not pinned:
            raise ValueError("Search Commands: no pinned commands")
            return
        
        # set active
        self.active = self.pinName
        pins.get()[self.pinName] = pinned
        
        # write to file
        pins.write()
       
    def pinClear(self):
        """
        Clear all pins and clear set selection.
        """
        # clear all pins
        for k, v in commands.get().iteritems():
            v["pin"] = False
         
        self.active = None

    def pinDelete(self):
        """
        Delete pin set, check if the provided name exists in the pin sets.
        If it does remove it from the data set and save.
        
        :raises ValueError: if name is invalid
        """
        if not self.pinName in pins.get().keys():
            raise ValueError("Search Commands: invalid name")
            return
        
        # pop from list
        pins.get().pop(self.pinName, None)
        self.pinClear()
        
        # write to file
        pins.write()

    # --------------------------------------------------------------------

    def refresh( self ):
        """
        Refresh command list and clear the pin set selection.
        """
        commands.store()
        self.pinClear()
        