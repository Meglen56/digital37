from maya.cmds import *
from PyQt4 import QtCore, QtGui
from checkTools import Ui_Frame
import re

class baseCheckTools(QtGui.QFrame):

    def __init__(self, uiBool, parent = None):
        QtGui.QFrame.__init__(self, parent)
        #super(baseCheckTools, self).__init__()
        self.boolUI = uiBool
        self.application = 'maya'
        self.version = '2012 x64'
        self.unit = 'cm'
        self.ui = Ui_Frame()
        self.ui.setupUi(self)
        if self.boolUI:
            self.c = QtGui.QColor(0, 255, 0)
            self.p = QtGui.QPalette(self.c)
        self.buttonConnect()
        
    def buttonConnect(self):
        self.ui.baseInfo.connect(self.ui.baseInfo, QtCore.SIGNAL("clicked()"), self.checkBaseInfo)
        self.ui.shapeAndTransformName.connect(self.ui.shapeAndTransformName, QtCore.SIGNAL("clicked()"), self.checkShapeTransName)
        self.ui.zeroObject.connect(self.ui.zeroObject, QtCore.SIGNAL("clicked()"), self.zeroObject)
        self.ui.doubleDisplay.connect(self.ui.doubleDisplay, QtCore.SIGNAL("clicked()"), self.doubleDisplay)
        self.ui.fiveFace.connect(self.ui.fiveFace, QtCore.SIGNAL("clicked()"), self.checkFiveFace)
        self.ui.reRangeUV.connect(self.ui.reRangeUV, QtCore.SIGNAL("clicked()"), self.checkUV)
        self.ui.deleteHistory.connect(self.ui.deleteHistory, QtCore.SIGNAL("clicked()"), self.deleteHistory)
        self.ui.deleteCamera.connect(self.ui.deleteCamera, QtCore.SIGNAL("clicked()"), self.deleteCamera)
        self.ui.deleteLight.connect(self.ui.deleteLight, QtCore.SIGNAL("clicked()"), self.deleteLight)
        self.ui.deleteDisplayLayer.connect(self.ui.deleteDisplayLayer, QtCore.SIGNAL("clicked()"), self.deleteDisplayLayer)
        self.ui.deleteRenderLayer.connect(self.ui.deleteRenderLayer, QtCore.SIGNAL("clicked()"), self.deleteRenderLayer)
        self.ui.deleteEmptyGroup.connect(self.ui.deleteEmptyGroup, QtCore.SIGNAL("clicked()"), self.deleteEmptyGroups)
        self.ui.unloadPlugin.connect(self.ui.unloadPlugin, QtCore.SIGNAL("clicked()"), self.unloadPlugins)
        self.ui.deleteUnknow.connect(self.ui.deleteUnknow, QtCore.SIGNAL("clicked()"), self.deleteUnknowNode)
        
    def checkBaseInfo(self):

        bool = True
        
        if(about(a = True) != self.application):
            if self.boolUI:
                self.ui.textEdit.insertPlainText("\napplication is error!\n")
            warning('application is error!')
            bool = False
        if(about(version = True) != self.version):
            if self.boolUI:
                self.ui.textEdit.insertPlainText("\nversion is error, must is 2011 x64\n")
            error('version is error, must is 2011 x64')
            bool = False
        if(currentUnit(q = True, l = True) != self.unit):
            if self.boolUI:
                self.ui.textEdit.insertPlainText("\ncurrent unit is error, must is cm\n")
            error('current unit is error, must is cm')
            bool = False

        if(bool):
            if self.boolUI:
                self.ui.baseInfo.setPalette(self.p)

    def checkShapeTransName(self):
    
        bool = True

        allObj = ls(type = ['mesh', 'nurbsSurface', 'subdiv'])
        for all in allObj:
            #print all
            try:
                if(len(all.split('|')) > 1):
                    if self.boolUI:
                        self.ui.textEdit.insertPlainText("\nmulti object have same name with %s\n" %all)
                    bool = False
            except:
                pass
            
            objParent = listRelatives(all, p = True)
            shape = ''
            tran = ''
            pat = re.compile('\D')
            every = pat.findall(all)
            for e in every:
                shape += e
            every = pat.findall(objParent[0])
            for e in every:
                tran += e
            if(not tran in shape):
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\n%s name dont match its parent name\n" %all)
                bool = False
        if(bool):
            if self.boolUI:
                self.ui.shapeAndTransformName.setPalette(self.p)
                
    def zeroObject(self):

        bool = True
    
        allObj = ls(type = ['mesh', 'nurbsSurface', 'subdiv'])
        for all in allObj:
            trans = listRelatives(all, p = True, f = True)
            try:
                makeIdentity(trans, a = True, t = True, r = True, s = True, n = 0)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\n%s zeroObject error\n" %trans)
                bool = False

        if(bool):
            if self.boolUI:
                self.ui.zeroObject.setPalette(self.p)
                
    def doubleDisplay(self):
        
        bool = True
        
        allObj = ls(type = ['mesh', 'nurbsSurface'])
        for all in allObj:
            try:
                select(all, r = True)
                displaySurface(two = True)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\nno object are selected in doubleDisplay, maybe cause by reference\n")
                bool = False
        select(cl = True)

        if(bool):
            if self.boolUI:
                self.ui.doubleDisplay.setPalette(self.p)
        
    def checkFiveFace(self):

        bool = True
        
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
                    if self.boolUI:
                        self.ui.textEdit.insertPlainText("\n%s f[%s] face more than four\n" %(dag, f))
                    bool = False
        if(bool):
            if self.boolUI:
                self.ui.fiveFace.setPalette(self.p)
                    
    def checkUV(self):

        bool = True
    
        allObj = ls(type = 'mesh')
        for all in allObj:
            try:
                polyNormalizeUV(all, nt = 1, pa = False)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\ndont normalize %s uv to 0-1 range\n" %all)
                bool = False

        if(bool):
            if self.boolUI:
                self.ui.reRangeUV.setPalette(self.p)
                    
    def deleteHistory(self):

        bool = True
    
        allObj = ls(type = ['mesh', 'nurbsSurface'])
        for all in allObj:
            try:
                delete(all, ch = True)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\ncant delete %s history\n" %all)
                bool = False

        if(bool):
            if self.boolUI:
                self.ui.deleteHistory.setPalette(self.p)
                
    def deleteCamera(self):
    
        allCam = listCameras()
        for all in allCam:
            if all != 'front' and all != 'persp' and all != 'side' and all != 'top':
                camera(all, e = True, sc = False)
                delete(all)
        if self.boolUI:
            self.ui.deleteCamera.setPalette(self.p)
                
    def deleteLight(self):
    
        bool = True
        
        allLight = ls(lights = True)
        for all in allLight:
            try:
                delete(all)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\ncant delete %s\n" %all)
                bool = False
                
        allLightLinker = ls(type = 'lightLinker')
        if(allLightLinker != ''):
            for all in allLightLinker:
                try:
                    lockNode(all, l  = False)
                    delete(all)
                except:
                    if self.boolUI:
                        self.ui.textEdit.insertPlainText("\ncant delete %s\n" %all)
                    bool = False

        if(bool):
            if self.boolUI:
                self.ui.deleteLight.setPalette(self.p)
                
    def deleteDisplayLayer(self):

        bool = True
    
        allDisLayer = ls(type = 'displayLayer')
        for all in allDisLayer:
            if(all != 'defaultLayer'):
                try:
                    delete(all)
                except:
                    if self.boolUI:
                        self.ui.textEdit.insertPlainText("\ncant delete %s\n" %all)
                    bool = False

        if(bool):
            if self.boolUI:
                self.ui.deleteDisplayLayer.setPalette(self.p)
                    
    def deleteRenderLayer(self):

        bool = True
    
        allRenderLayer = ls(type = 'renderLayer')
        for all in allRenderLayer:
            if(all != 'defaultRenderLayer'):
                try:
                    editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    delete(all)
                except:
                    if self.boolUI:
                        self.ui.textEdit.insertPlainText("\ncant delete %s\n" %all)
                    bool = False

        if(bool):
            if self.boolUI:
                self.ui.deleteRenderLayer.setPalette(self.p)
            
    def deleteEmptyGroups(self):

        bool = True

        allTran = ls(type = 'transform')
        for all in allTran:
            try:
                child = listRelatives(all, c = True)
                if(child == None):
                    delete(all)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\ncant delete %s\n" %all)
                bool = False
        if(bool):
            if self.boolUI:
                self.ui.deleteEmptyGroup.setPalette(self.p)
                    
    def unloadPlugins(self):

        bool = True
    
        allPlugin = pluginInfo(q = True, ls = True)
        for all in allPlugin:
            if('tomr' in all or 'Turtle' in all or '3dlight' in all or 'RenderMan' in all):
                try:
                    unloadPlugin(all, f = True)
                except:
                    if self.boolUI:
                        self.ui.textEdit.insertPlainText("\ncant unload plugin %s, because some object are used this plugin\n" %all)
                    bool = False

        if(bool):
            if self.boolUI:
                self.ui.unloadPlugin.setPalette(self.p)

    def deleteUnknowNode(self):

        bool = True

        allUnknow = ls(dep = True)
        for all in allUnknow:
            try:
                if(nodeType(all) == 'unknow'):
                    lockNode(all, l = False)
                    delete(all)
            except:
                if self.boolUI:
                    self.ui.textEdit.insertPlainText("\ncant delete unknow node %s\n" %all)
                bool = False
        if self.boolUI:
            self.ui.deleteUnknow.setPalette(self.p)
            
    def doAll(self):
        
        self.checkBaseInfo()
        self.checkShapeTransName()
        self.zeroObject()
        self.doubleDisplay()
        self.checkFiveFace()
        self.checkUV()
        self.deleteHistory()
        self.deleteCamera()
        self.deleteLight()
        self.deleteDisplayLayer()
        self.deleteRenderLayer()
        self.unloadPlugins()
        self.deleteUnknowNode()
        
def main(bool):
    global modelBaseCheckTools
    modelBaseCheckTools = baseCheckTools(bool)
    if(bool):
        modelBaseCheckTools.show()
    else:
        modelBaseCheckTools.doAll()