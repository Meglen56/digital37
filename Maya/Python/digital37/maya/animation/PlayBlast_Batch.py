import maya.cmds as cmds

#use evalDeferred to do palyblast
def main(frameInfo='Z:/D031SEER/QC/techical/anim/Frames_All.txt',outputDir='d:/seer/pb/'):
    cmd = list()
    cmd.append('import digital37.maya.animation.PerformPlayBlast')
    cmd.append('digital37.maya.animation.PerformPlayBlast.main('+'\"' + frameInfo + '\",\"' + outputDir + '\"' + ')')
    cmd = '\n'.join(cmd)
    print cmd
    cmds.evalDeferred(cmd)