import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    dagNode = cmds.ls(dag = True, type = 'mesh')
    for dag in dagNode:
        cmds.select(dag)
        numFace = cmds.polyEvaluate(f = True)
        for f in range(0, numFace):
            allEdge = []
            cmds.select(cl = True)
            cmds.select(dag + '.f[' + str(f) + ']')
            edgeNum = cmds.polyInfo(fe = True)
            eSplit1 = edgeNum[0].split(':')
            eSplit2 = eSplit1[1].split(' ')
            for e in eSplit2:
                if(e != ''):
                    allEdge.append(e)
            if(len(allEdge) > 5):
                loger.error("%s f[%s] face more than four" %(dag, f))