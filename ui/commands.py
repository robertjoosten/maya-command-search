from . import utils
    
# ----------------------------------------------------------------------------
    
PIN_ICON = ":/nodeGrapherPinnedLarge.png"
UNPIN_ICON = ":/nodeGrapherUnpinnedLarge.png"
OPTION_ICON = ":/hsNothing.png"

# ----------------------------------------------------------------------------
    
class Commands(utils.QWidget):
    """
    Commands
    
    The commands widget is the widget that gets populated with the searched
    commands.
    
    :param QWidget parent:
    """
    def __init__(self, parent=None):
        utils.QWidget.__init__(self, parent)
        
        # variable
        self.parent = parent

        # create layout
        layout = utils.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # create scroll area
        scrollArea = utils.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(utils.Qt.ScrollBarAlwaysOff)
        
        # create main widget widget
        self.widget = utils.QWidget()
        
        # create main layout
        self.layout = utils.QVBoxLayout(self.widget)
        self.layout.setContentsMargins(3,0,3,0)
        self.layout.setSpacing(0)

        scrollArea.setWidget(self.widget)
        layout.addWidget(scrollArea)
        
        # spacer
        spacer = utils.QSpacerItem(
            1, 
            1, 
            utils.QSizePolicy.Minimum,
            utils.QSizePolicy.Expanding
        )
        self.layout.addItem(spacer)
        
    # ------------------------------------------------------------------------
        
    def clear(self):
        for i in reversed(range(self.layout.count()-1)):
            item = self.layout.itemAt(i)
            item.widget().deleteLater()
    
    def populate(self, matches):
        """
        Populate widget with commands from input.
        
        :param list matches: Command list
        """
        # clear
        self.clear()
    
        # filter
        previousGroup = None
        for match in matches:
            # create group divider
            group = match.get("group")
            if group != previousGroup:
                divider = utils.Divider(self.widget, group)
                self.add(divider)
                 
            # create command
            button = Button(self.widget, match)
            self.add(button)
            previousGroup = group
            
    # ------------------------------------------------------------------------
    
    def add(self, widget):
        """
        Add widget to layout, inserts it at -1 as there is always a spacer
        that needs to remain at the bottom.
        
        :param QWidget widget:
        """
        self.layout.insertWidget(self.layout.count() - 1, widget)
        
    def isEmpty(self):
        """
        Check if the widgets layout is empty.
        
        :rtype: bool
        """
        return self.layout.isEmpty()

class Button(utils.QWidget):
    """
    Button
    
    This widget gets initialized with the command data and builds it
    accordingly, the only variable option is the option box that may
    or may not be added into the info.
    
    :param QWidget parent:
    :param dict info:
    """
    def __init__(self, parent, info):
        utils.QWidget.__init__(self, parent)

        # variable
        self.info = info
        self.setFixedHeight(20)
        
        # style sheet
        basicSS = "QPushButton{text-align: left;}"
        hoverSS1 = "QPushButton:hover{ \
            border: 1px solid orange; \
            border-radius: 3px; \
            background-color: orange; \
        }"
        hoverSS2 = "QPushButton:hover{color: orange;}"
        
        # get exec
        self.command = info.get("cmd")
        self.commandOption = info.get("cmdOption")
        
        # create pin
        self.pin = utils.QPushButton(self)
        self.pin.setStyleSheet(hoverSS1)
        self.setAsIcon(self.pin)
        
        # create icon
        icon = utils.QPushButton(self)
        icon.setIcon(info.get("icon"))
        icon.released.connect(self.exec_)
        self.setAsIcon(icon)
        
        # create main
        main = utils.QPushButton(info.get("name"), self)
        main.setFixedHeight(20)
        main.setStyleSheet(basicSS + hoverSS2)
        main.setFlat(True)
        main.setToolTip(info.get("hierarchy"))
        main.released.connect(self.exec_)

        # create layout
        layout = utils.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # add widgets
        layout.addWidget(self.pin)
        layout.addWidget(icon)
        layout.addWidget(main)
        
        # create option box
        if self.commandOption:
            option = utils.QPushButton(self)
            option.setStyleSheet(hoverSS1)
            option.setIcon(utils.QIcon(OPTION_ICON))
            option.pressed.connect(self.execOption_)
            self.setAsIcon(option)
            layout.addWidget(option)
            
        # set pin
        if info.get("pin"):         self.setPin()
        else:                       self.setUnpin()
            
    # ------------------------------------------------------------------------
    
    def setAsIcon(self, b):
        """
        Sometimes a command will have an icon assigned to it, to make sure 
        the button looks like an icon this function can be used, to set those
        attributes.
        
        :param QPushButton b:
        """
        b.setFixedWidth(20)
        b.setFixedHeight(20)
        b.setFlat(True)
        b.setIconSize(utils.QSize(18,18))  
          
    # ------------------------------------------------------------------------
        
    def setPin(self):
        self.info["pin"] = True
        self.pin.setIcon(utils.QIcon(PIN_ICON))
        self.pin.pressed.connect(self.setUnpin)

    def setUnpin(self):
        self.info["pin"] = False
        self.pin.setIcon(utils.QIcon(UNPIN_ICON))
        self.pin.pressed.connect(self.setPin)
        
    # ------------------------------------------------------------------------
         
    def exec_(self):
        if not self.command:
            return
            
        self.command.trigger()
   
    def execOption_(self):
        if not self.commandOption:
            return
            
        self.commandOption.trigger()