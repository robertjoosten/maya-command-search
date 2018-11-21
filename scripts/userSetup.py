import maya.cmds as cmds

if not cmds.about(batch=True):
    import commandSearch
    cmds.evalDeferred(commandSearch.install)
