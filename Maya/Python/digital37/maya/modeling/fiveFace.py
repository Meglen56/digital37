import maya.cmds as cmds
import logging

def main():

    loger = logging.getLogger()
    
    dagNode = ls(dag = True, type = 'mesh')
    for dag in dagNode:
        select(dag)
        numFace = polyEvaluate(f = True)
        for f in range(0, numFace):
            allEdge = []
            select(cl = True)
            select(dag + '.f[' + str(f) + ']')
            edgeNum = polyInfo(fe = True)
            eSplit1 = edgeNum[0].split(':')
            eSplit2 = eSplit1[1].split(' ')
            for e in eSplit2:
                if(e != ''):
                    allEdge.append(e)
            if(len(allEdge) > 5):
                loger.error("%s f[%s] face more than four" %(dag, f))