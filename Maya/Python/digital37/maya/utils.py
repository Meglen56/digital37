import os

import pymel.core as pm

import maya.OpenMayaUI as mui
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import sip

import grid.path

def snapTrans (parent=[],child=None):
    '''
    Snap the last selected object in translation.
    '''
    if not parent :
        selectedObj = pm.selected()
        parent = selectedObj[:-1]
        child = selectedObj[-1]
        
    pm.delete(pm.pointConstraint(parent, child, maintainOffset=False))
    
def snapRot (parent=[],child=None):
    '''
    Snap the last selected object in rotation.
    '''
    if not parent :
        selectedObj = pm.selected()
        parent = selectedObj[:-1]
        child = selectedObj[-1]
        
    pm.delete(pm.orientConstraint(parent, child, maintainOffset=False))
    
def lockAndHide (node,lock=True,hide=True,visibility=False):
    '''
    Lock and Hide the attribute of node.
    
    Param :
    node = DAG node
    lock = Boolean
    hide = Boolean
    visibility = Boolean
    '''
    if not visibility :
        for attr in node.listAttr(keyable=True) :
            if not "visibility" in str(attr) :
                if lock :
                    attr.lock()
                if hide :
                    attr.setKeyable(False)
    else :
        for attr in node.listAttr(keyable=True) :
            if lock :
                attr.lock()
            if hide :
                attr.setKeyable(False)
                
def unlockAndUnhide (nodeList=[]):
    '''
    Unlock and Unhide the classic keyable attribute of the selected nodes.
    
    Param :
    nodeList
    '''
    for node in nodeList :
        for attribute in ['tx','ty','tz','rx','ry','rz','sx','sy','sz','visibility'] :
            node.attr(attribute).unlock()
            node.attr(attribute).setKeyable(True)
                
def listWorldChildren ():
    '''
    Return the transform node at the root of the hierarchy.
    
    Return :
    worldChildrenList = List
    '''
    worldChildrenList = list()
    for elem in pm.ls(assemblies=True) :
        if pm.nodeType(elem) == 'transform' :
            worldChildrenList.append(elem)
    return worldChildrenList


def getTimelineFrameRange():
    '''
    Return the timeline frame range of the scene
    
    Return :
    startFrame = int
    endFrame = int
    '''
    startFrame = pm.playbackOptions (q=True,minTime =True)
    endFrame = pm.playbackOptions (q=True,maxTime =True)
    return startFrame,endFrame

def listNotUniqueName (batch=False):
    '''
    Return a list of the nodes that don't have a unique name
    '''
    notUniqueNameList = list()
    for node in pm.ls() :
        if '|' in str(node) :
            notUniqueNameList.append(node)
            
    if len(notUniqueNameList) == 0 :
        print 'All Nodes name OK'
    else :
        for node in notUniqueNameList :
            print node
    return notUniqueNameList

def deleteUnknownNode ():
    '''
    Delete unknown Nodes.
    '''
    for unknownNode in pm.ls(type='unknown') :
        try :
            deletedNodeName = str(unknownNode)
            pm.delete(unknownNode)
            print 'Delete :', deletedNodeName
        except :
            pass
        
def getTopGNodeList ():
    '''
    Return the gAsset Node and the gShotNode at the top of the hierarchy
    '''
    topGNodeList = list()
    for node in pm.ls(assemblies=True):
        if node.nodeType() == 'gAsset' or node.nodeType() == 'gShot' :
            topGNodeList.append(node)
    return topGNodeList
        

def getMayaWindow():
    #Get the maya main window as a QMainWindow instance
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


def selectCharAllControl (nameSpace, addToSelection=False) :
    '''
    Select all the controler of a character.
    '''
    if not addToSelection :
        pm.select(cl=True)
        try :
            pm.select('%s:*CD'%nameSpace)
        except :
            pass
    else :
        try :
            pm.select('%s:*CD'%nameSpace,tgl=True)
        except :
            pass
        
    try :
        pm.select('%s:*GD'%nameSpace,tgl=True)
    except :
        pass
    try :
        pm.select('%s:*ctrl'%nameSpace,tgl=True)
    except :
        pass
    
def isShotScene ():
    sceneName = grid.path.path(pm.system.sceneName()).namebase
    if sceneName.startswith('Sq') and pm.nodeType(getTopGNodeList()[0]) == 'gShot' :
        return True
    else :
        return False
    
def getShotNumberFromName ():
    sceneName = grid.path.path(pm.system.sceneName()).namebase
    if isShotScene () :
        sequenceNumber = int(sceneName.split('_')[0][2:])
        shotNumber = int(sceneName.split('_')[1][2:])
    else :
        raise Exception, 'This scene is not a shot'
    return sequenceNumber, shotNumber

def getShotNode ():
    if isShotScene() :
        return getTopGNodeList()[0]
    else :
        raise Exception, 'This scene is not a shot'
    
def checkShotNumber (batch=False, copyFromFileName=False):
    getShotNode ().checkShotNumber(batch=batch, copyFromFileName=copyFromFileName)
    
def getReticle ():
    return pm.ls(type='spReticleLoc')[0]

def getProjectRoot(project='SNAP_PROJECT'):
    return grid.path.path(os.environ[project])
        
    

    
    