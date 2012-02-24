from maya.cmds import *
import re

class baseCheckTools():

    application = ''
    version = ''
    unit = ''
    ui = ''

    def __init__(self, uiName):

        self.application = 'maya'
        self.version = '2012 x64'
        self.unit = 'cm'
        self.ui = uiName
        #button(self.ui + '|pushButton1', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton2', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton3', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton4', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton5', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton6', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton7', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton8', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton9', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton10', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton11', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton12', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton13', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton14', e = True, bgc = (1.0, 0.0, 0.0))
        #button(self.ui + '|pushButton15', e = True, bgc = (1.0, 0.0, 0.0))
        
    def checkBaseInfo(self):

        bool = True
        
        if(about(a = True) != self.application):
            scrollField(self.ui + '|textEdit', e = True, it = '\napplication is error!\n')
            warning('application is error!')
            bool = False
        if(about(version = True) != self.version):
            scrollField(self.ui + '|textEdit', e = True, it = '\nversion is error, must is 2012 x64\n')
            error('version is error, must is 2012 x64')
            bool = False
        if(currentUnit(q = True, l = True) != self.unit):
            scrollField(self.ui + '|textEdit', e = True, it = '\ncurrent unit is error, must is cm\n')
            error('current unit is error, must is cm')
            bool = False

        if(bool):
            button(self.ui + '|pushButton1', e = True, bgc = (0.0, 1.0, 0.0))

    def checkShapeTransName(self):
    
        bool = True

        allObj = ls(type = ['mesh', 'nurbsSurface', 'subdiv'])
        for all in allObj:
            #print all
            try:
                if(len(all.split('|')) > 1):
                    scrollField(self.ui + '|textEdit', e = True, it = '\nmulti object have same name with %s\n' %all)
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
                scrollField(self.ui + '|textEdit', e = True, it = '\n%s name dont match its parent name\n' %all)
                bool = False
        if(bool):        
            button(self.ui + '|pushButton2', e = True, bgc = (0.0, 1.0, 0.0))
                
    def zeroObject(self):

        bool = True
    
        allObj = ls(type = ['mesh', 'nurbsSurface', 'subdiv'])
        for all in allObj:
            trans = listRelatives(all, p = True, f = True)
            try:
                makeIdentity(trans, a = True, t = True, r = True, s = True, n = 0)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\n%s zeroObject error\n' %trans)
                bool = False

        if(bool):
            button(self.ui + '|pushButton3', e = True, bgc = (0.0, 1.0, 0.0))
                
    def doubleDisplay(self):
        
        bool = True
        
        allObj = ls(type = ['mesh', 'nurbsSurface'])
        for all in allObj:
            try:
                select(all, r = True)
                displaySurface(two = True)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\nno object are selected in doubleDisplay, maybe cause by reference\n')
                bool = False
        select(cl = True)

        if(bool):
            button(self.ui + '|pushButton4', e = True, bgc = (0.0, 1.0, 0.0))
        
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
                    scrollField(self.ui + '|textEdit', e = True, it = '\n%s f[%s] face more than four\n' %(dag, f))
                    bool = False
        if(bool):
            button(self.ui + '|pushButton5', e = True, bgc = (0.0, 1.0, 0.0))
                    
    def checkUV(self):

        bool = True
    
        allObj = ls(type = 'mesh')
        for all in allObj:
            try:
                polyNormalizeUV(all, nt = 1, pa = False)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\ndont normalize %s uv to 0-1 range\n' %all)
                bool = False

        if(bool):
            button(self.ui + '|pushButton6', e = True, bgc = (0.0, 1.0, 0.0))
                    
    def deleteHistory(self):

        bool = True
    
        allObj = ls(type = ['mesh', 'nurbsSurface'])
        for all in allObj:
            try:
                delete(all, ch = True)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete %s history\n' %all)
                bool = False

        if(bool):
            button(self.ui + '|pushButton7', e = True, bgc = (0.0, 1.0, 0.0))
                
    def deleteCamera(self):
    
        allCam = listCameras()
        for all in allCam:
            if all != 'front' and all != 'persp' and all != 'side' and all != 'top':
                camera(all, e = True, sc = False)
                delete(all)

        button(self.ui + '|pushButton8', e = True, bgc = (0.0, 1.0, 0.0))
                
    def deleteLight(self):
    
        bool = True
        
        allLight = ls(lights = True)
        for all in allLight:
            try:
                delete(all)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete %s\n' %all)
                bool = False
                
        allLightLinker = ls(type = 'lightLinker')
        if(allLightLinker != ''):
            for all in allLightLinker:
                try:
                    lockNode(all, l  = False)
                    delete(all)
                except:
                    scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete %s\n' %all)
                    bool = False

        if(bool):
            button(self.ui + '|pushButton9', e = True, bgc = (0.0, 1.0, 0.0))
                
    def deleteDisplayLayer(self):

        bool = True
    
        allDisLayer = ls(type = 'displayLayer')
        for all in allDisLayer:
            if(all != 'defaultLayer'):
                try:
                    delete(all)
                except:
                    scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete %s\n' %all)
                    bool = False

        if(bool):
            button(self.ui + '|pushButton10', e = True, bgc = (0.0, 1.0, 0.0))
                    
    def deleteRenderLayer(self):

        bool = True
    
        allRenderLayer = ls(type = 'renderLayer')
        for all in allRenderLayer:
            if(all != 'defaultRenderLayer'):
                try:
                    editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    delete(all)
                except:
                    scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete %s\n' %all)
                    bool = False

        if(bool):
            button(self.ui + '|pushButton11', e = True, bgc = (0.0, 1.0, 0.0))
            
    def deleteEmptyGroups(self):

        bool = True

        allTran = ls(type = 'transform')
        for all in allTran:
            try:
                child = listRelatives(all, c = True)
                if(child == None):
                    delete(all)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete %s\n' %all)
                bool = False
        if(bool):
            button(self.ui + '|pushButton12', e = True, bgc = (0.0, 1.0, 0.0))
                    
    def unloadPlugins(self):

        bool = True
    
        allPlugin = pluginInfo(q = True, ls = True)
        for all in allPlugin:
            if('tomr' in all or 'Turtle' in all or '3dlight' in all or 'RenderMan' in all):
                try:
                    unloadPlugin(all, f = True)
                except:
                    scrollField(self.ui + '|textEdit', e = True, it = '\ncant unload plugin %s, because some object are used this plugin\n' %all)
                    bool = False

        if(bool):
            button(self.ui + '|pushButton14', e = True, bgc = (0.0, 1.0, 0.0))

    def deleteUnknowNode(self):

        bool = True

        allUnknow = ls(dep = True)
        for all in allUnknow:
            try:
                if(nodeType(all) == 'unknown'):
                    lockNode(all, l = False)
                    delete(all)
            except:
                scrollField(self.ui + '|textEdit', e = True, it = '\ncant delete unknow node %s\n' %all)
                bool = False

        button(self.ui + '|pushButton15', e = True, bgc = (0.0, 1.0, 0.0))
            
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
