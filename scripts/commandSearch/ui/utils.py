import os
from maya import OpenMayaUI, cmds, mel

# import pyside, do qt version check for maya 2017 >
qtVersion = cmds.about(qtVersion=True)
if qtVersion.startswith("4") or type(qtVersion) not in [str, unicode]:
    from PySide.QtGui import *
    from PySide.QtCore import *
    import shiboken
else:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import shiboken2 as shiboken
    
# ----------------------------------------------------------------------------
  
FONT = QFont()
FONT.setFamily("Consolas")

BOLT_FONT = QFont()
BOLT_FONT.setFamily("Consolas")
BOLT_FONT.setWeight(100)  

# -----------------------------------------------------------------------------    
    
def mayaWindow():
    """
    Get Maya's main window.
    
    :rtype: QMainWindow
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = shiboken.wrapInstance(long(window), QMainWindow)
    
    return window
    
def mayaMenu():
    """
    Find Maya's main menu bar.
    
    :rtype: QMenuBar
    """
    for m in mayaWindow().children():
        if type(m) == QMenuBar:
            return m
    
# ----------------------------------------------------------------------------
    
def mayaToQT(name):
    """
    Maya -> QWidget

    :param str name: Maya name of an ui object
    :return: QWidget of parsed Maya name
    :rtype: QWidget
    """
    ptr = OpenMayaUI.MQtUtil.findControl(name)
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findLayout(name)    
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findMenuItem(name)
    if ptr is not None:     
        return shiboken.wrapInstance(long(ptr), QWidget)
    
def qtToMaya(widget):
    """
    QWidget -> Maya name

    :param QWidget widget: QWidget of a maya ui object
    :return: Maya name of parsed QWidget
    :rtype: str
    """
    return OpenMayaUI.MQtUtil.fullName(
        long(
            shiboken.getCppPointer(widget)[0]
        ) 
    )
    
# ----------------------------------------------------------------------------

def getStatusLine():
    """
    Get the QWidget of Maya's status line. 
    
    :return: QWidget of Maya's status line
    :rtype: QWidget
    """
    gStatusLine = mel.eval("$tmpVar=$gStatusLine")
    return mayaToQT(gStatusLine)

# ----------------------------------------------------------------------------

def findSearchIcon():
    """
    Loop over all paths in the XBMLANGPATH variable and see if custom icon
    can be found, if this is not the case a maya default one will be returned.
    
    :return: CMD search icon.
    :rtype: QIcon
    """
    # construct all icon paths
    paths = []
    if os.environ.get("XBMLANGPATH"):
        paths = os.environ.get("XBMLANGPATH").split(os.pathsep)
    paths.append(os.path.join(os.path.split(__file__)[0], "icons"))

    # find icon
    for path in paths:
        filepath = os.path.join(path, "rjCMDSearch.png")
        if os.path.exists(filepath):
            return QIcon(filepath)
            
    return QIcon(":/cmdWndIcon.png")  
    
# ----------------------------------------------------------------------------   

class Divider(QWidget):     
    """
    Divider widget that is used in the manager menu and the commands overview.
    
    :param QWidget parent:
    :param str group: Name to be used in the divider
    """
    def __init__(self, parent, group):
        QWidget.__init__(self, parent)
        
        # style sheets
        labelSS = "QLabel{font: bold; color: orange; border: 0px;}"
        frameSS = "QFrame{color: gray; margin: 0 12 0 12;}"
        
        # create widgets
        label = QLabel(self)
        label.setText(group)
        label.setFixedHeight(12)
        label.setStyleSheet(labelSS)
        
        sep01 = QFrame(self)
        sep02 = QFrame(self)
        
        for sep in [sep01,sep02]:
            sep.setStyleSheet(frameSS)
            sep.setFrameStyle(QFrame.HLine)
            sep.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # create layout
        layout = QHBoxLayout(self)
        layout.addWidget(sep01)
        layout.addWidget(label)
        layout.addWidget(sep02)
                
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setFixedHeight(12)