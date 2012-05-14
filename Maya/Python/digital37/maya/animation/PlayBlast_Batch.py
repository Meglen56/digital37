import maya.cmds as cmds

#use evalDeferred to do palyblast
cmds.evalDeferred('import PerformPlayBlast\nPerformPlayBlast.main()')