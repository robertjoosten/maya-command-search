from . import utils
from . import commands

# ----------------------------------------------------------------------------

MENU_MAX_RESULTS = 20

# ----------------------------------------------------------------------------
    
class ResultsMenu(utils.QMenu):
    """
    Results Menu
    
    Used to display the commands widget as a menu that is positioned
    underneath the search widget.
    
    :param QWidget parent:
    """
    aboutToClose = utils.Signal()
    def __init__(self, parent=None):
        utils.QMenu.__init__(self, parent)
        
        # variable
        self.parent = parent
        
        self.setTearOffEnabled( True )
        self.setFixedWidth(250)
        self.setMaximumWidth(250)
        self.setMaximumHeight(MENU_MAX_RESULTS*24)

        # create widget
        self.widget = commands.Commands(self)
        self.widget.setMaximumHeight(MENU_MAX_RESULTS*24)
        
        # add to menu
        action = utils.QWidgetAction(self)
        action.setDefaultWidget(self.widget)
        self.addAction(action)
        
    # ------------------------------------------------------------------------
    
    def keyPressEvent(self, e):
        self.parent.search.keyPressEvent(e)
    
    def mouseReleaseEvent( self, e ):
        # process click
        cursor = utils.QCursor.pos()
        menu = self.pos()

        x = menu.x() <= cursor.x() <= (menu.x() + 250)
        y = menu.y() <= cursor.y() <= (menu.y() + 12)
        
        # process if in right area
        if not x or not y:
            return
            
        # switch current   
        self.aboutToClose.emit()

    # ------------------------------------------------------------------------
        
    def position(self):
        """
        Position the menu underneath the search widget, the position is 
        queried from the parent widget.
        """
        pos = self.parent.parentWidget().mapToGlobal(self.parent.pos())
        posX = pos.x()
        posY = pos.y()
        height = self.parent.height()
        
        posY += height
        self.move(posX+8, posY)  
        
    # ------------------------------------------------------------------------

    def show(self, num):
        # hide if empty
        if not num:   
            self.hide()
            return
    
        # position
        self.position()

        # show menu
        utils.QMenu.show(self)  
            
class ResultsWindow(utils.QDockWidget):
    """
    Results Menu
    
    Used to display the commands widget as a window that can be docked to
    Maya's native ui.
    
    :param QWidget parent:
    """
    aboutToClose = utils.Signal()
    def __init__(self, parent=None):
        utils.QDockWidget.__init__(self, parent)
        
        # variable
        self.parent = parent
        self.setAllowedAreas(
            utils.Qt.RightDockWidgetArea|utils.Qt.LeftDockWidgetArea
        )
        
        self.setParent(parent)        
        self.setWindowFlags(utils.Qt.Window)  
        self.setWindowTitle("Search Commands")
        self.resize(250, 500)
        
        cw = utils.QWidget(self)
        self.setWidget(cw)
        
        # create layout
        layout = utils.QHBoxLayout(cw)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # create widget
        self.widget = commands.Commands(cw)
        layout.addWidget(self.widget)
        
        # add widget
        #utils.mayaWindow().addDockWidget(Qt.RightDockWidgetArea, self)
        
    # ------------------------------------------------------------------------
    
    def keyPressEvent(self, e):
        self.parent.search.keyPressEvent(e)
        
    def closeEvent(self, e):
        self.aboutToClose.emit()
        utils.QDockWidget.closeEvent(self, e)
        
    # ------------------------------------------------------------------------
        
    def show(self, num):
        utils.QDockWidget.show(self)
        