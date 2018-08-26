from . import ui, decorators


@decorators.getCommandSearch  
def focus(commandSearch):
    """
    Set focus to the input search field of the command search widget. Will
    return early if either the results window or the search bar already
    has focus.
    
    :param SearchWidget commandSearch: decorator handles this argument
    """
    if commandSearch.search.hasFocus() or commandSearch.results.hasFocus():
        return

    ui.mayaWindow().activateWindow()
    commandSearch.enter()