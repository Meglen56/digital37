import os
from workflowBase import *
from maya.cmds import *
import maya.mel as mm

class makeCache(workflowBase):
    '''
    Steps
    1 Save original file
    2 Get file info: 
        1 Reference file list, time
        2 Deformed shape node list (no intermediate)
        3 Transform node list
        4 Get attribute value and keyed attribute
    3 Set Display: don't display scene objects
    4 Create geo cache of every reference file:
        1 Create geo cache
    5 Recorder keyed attribute
    6 New file
    7 Reference file
    8 Set attribute value
    9 Create animation
    10 Import geo cache
    11 Save file
    setNamedPanelLayout "Single Perspective View";
    modelEditor('modelPanel4',e=1,allObjects=0)
    '''
    
    sTime = 0.0
    eTime = 0.0
    geoCacheDir = ''
    cacheDir = ''
    cacheFileName = ''
    refInfoName = ''
    valInfoName = ''
    keyInfoName = ''
    timeInfoName = ''
    origShapeInfoName = ''
    refs = []
    selectedRefs = []
    shot = ''
    texModFiles = []
    #dShapes = []
    #cShapes = {}
    #tNodes = []
    #nkAttrs = {}
    #kAttrs = {}
    
    defaultAttrName = ('.tx','.ty','.tz',
                       '.rx','.ry','.rz',
                       '.sx','.sy','.sz','.v')
    def __init__(self,ruleManager):
        workflowBase.__init__(self,ruleManager)
        
        # Values
        print '====== File Info ===================='
        # Shot
        sn = file(q=1,sn=1,shn=1)#.split('.')[0]
        self.shot = self.R.path2assetName(sn)
        print '      Shot Name:',self.shot
        # geoCacheDir & cacheDir
        self.geoCacheDir = self.R.getPath_geoCache(self.shot)#self.R.pipeline['DynamicGeoCache'] + '/' + self.shot
        self.cacheDir = self.R.getPath_cache(self.shot)#self.R.pipeline['Dynamic'] + '/' + self.shot
        print '   geoCache Dir:',self.geoCacheDir
        print '      Cache Dir:',self.cacheDir
        # cacheFileName
        self.cacheFileName = self.RM.getFileName(self.shot)#'cf_cache_shot000_fin_lx.mb'
        self.refInfoName = '%s_ref.inf' % self.shot
        self.valInfoName = '%s_val.inf' % self.shot
        self.keyInfoName = '%s_key.inf' % self.shot
        self.timeInfoName = '%s_time.inf' % self.shot
        self.origShapeInfoName = '%s_specialDeformedShape.inf' % self.shot
        print 'Cache File Name:',self.cacheFileName
        
        # Refs
        self.refs = file(q=1,r=1)
        # TexModFiles - Get it from ani file
        self.texModFiles = {}
        for ref in self.refs:
            ns = file(ref,q=1,namespace=1)
            tm = self.R.riggingFile2textureModelFile(ref)
            print '==== Ref ====:',ref
            print '    Namespace:',ns
            print 'Shading Model:',tm
            self.texModFiles[ns] = (tm)
        # sTime & eTime
        self.sTime = playbackOptions(q=1,min=1) - self.R.extTime
        self.eTime = playbackOptions(q=1,max=1) + self.R.extTime
        print 'Start time:',self.sTime
        print '  End time:',self.eTime
        # time unit
        #self.R.timeUnit = currentUnit(q=1,t=1)
        
    def isDefaultValue(self,attr,value):
        elem = attr.rsplit('.',1)
        attrName = '.'+elem[1]
        if attrName in ('.tx','.ty','.tz','.rx','.ry','.rz'):
            if value == 0:
                return 1
            else:
                return 0
        if attrName in ('.sx','.sy','.sz','.v'):
            if value == 1:
                return 1
            else:
                return 0
    def createTime(self):
        # 1 - Create dir
        if not os.path.isdir(self.cacheDir):
            os.mkdir(self.cacheDir)
        # 2 - Create new file
        name = self.cacheDir + '/' + self.timeInfoName
        f = open(name,'w')
        f.writelines('%s %s'%(self.sTime,self.eTime))
        f.close()
    def createModelList(self):
        # 1 - Create dir
        if not os.path.isdir(self.cacheDir):
            os.mkdir(self.cacheDir)
        # 2 - Create new file
        name = self.cacheDir + '/' + self.refInfoName
        f = open(name,'w')
        for ns in self.texModFiles.keys():
            path = self.texModFiles[ns]
            f.writelines('%s %s\r\n'%(ns,path))
        f.close()
    def createSpecialDeformedShapeList(self):
        # Get deformed shapes
        dShapes = ls('*Deformed',type=self.R.shapeType)
        if dShapes==[]:
            return
        print 'Find the special deformed shape...'
        # 1 - Create dir
        if not os.path.isdir(self.cacheDir):
            os.mkdir(self.cacheDir)
        # 2 - Create new file
        name = self.cacheDir + '/' + self.origShapeInfoName
        f = open(name,'w')
        for dShape in dShapes:
            f.writelines('%s %s\r\n'%(dShape,self.__getOrigNode__(dShape)))
        f.close()
    def __getOrigNode__(self,shape):
        t = objectType(shape)
        nodes = listHistory(shape)
        nodes = ls(nodes,type=t)
        return nodes[1]
    def getTrueShape(self,shape):
        if shape.endswith('Deformed'):
            print 'Get true shape:',shape
            name = self.cacheDir + '/' + self.origShapeInfoName
            lines = []
            try:
                F = open(name,'r')
                lines = F.readlines()
                F.close()
            except:
                print ">>>>> Can't open file:",name
                return shape
            for line in lines:
                item = line.split(' ')
                if shape==item[0]:
                    return item[1].strip()
        return shape
    def __doCreateGeoCache__(self,refs):
        # refs = string[] or string
        if type(refs)!=type([]) and type(refs)!=type(()):
            refs = [refs]
        for refFile in refs:
            print 'Ref File:',refFile
            ns = self.R.path2namespace(refFile)
            # 1 - Get shapes
            shapes = self.R.getHighModelShapes(refFile)
            #shapes = self.R.getLowModelShapes(refFile)
            if shapes==[]:
                print '>>>>> Not the shape'
            else:
                #print 'shapes:',shapes
                '''
                rShapes = []
                for shape in shapes:
                    if self.R.isRenderableShape(shape):
                        rShapes.append(shape)
                '''
                # 2 - Get deformed shapes
                dShapes = []
                for shape in shapes:
                    if self.R.isDeformedShape(shape):
                        dShapes.append(shape)
                #print 'Deformed Shapes:',dShapes
                if dShapes == []:
                    print '>>>>> Not the deformed shape'
                # 3 - Create geo cache
                else:
                    print '====== Do geo cache ======'
                    print 'Dir:',self.geoCacheDir
                    xml = cacheFile(staticCache=1,
                                    dir=self.geoCacheDir,
                                    f = ns,
                                    format='OneFilePerFrame',#OneFile
                                    sch = 1,
                                    st=self.sTime, et=self.eTime,
                                    points=dShapes)
                    print 'XML:',xml
        self.createSpecialDeformedShapeList()
    def createGeoCache(self):
        print '====== Create Geo Cache ===================='
        self.__doCreateGeoCache__(self.refs)
    def createSelectedGeoCache(self):
        #refs = string[] or string
        print '====== Create Geo Cache ===================='
        self.__doCreateGeoCache__(self.selectedRefs)
    def createKeyCache(self):
        kAttrs = {}
        nkAttrs = {}
        print '====== Create Key Cache ======================='
        for refFile in self.refs:
            # 2 - Get transform nodes
            tNodes = self.R.getHighModelTransformNodes(refFile)
            #tNodes = self.R.getLowModelTransformNodes(refFile)
            for node in tNodes:
                #print 'node:',node
                # 3 - Get value and keyed attributes
                for item in self.defaultAttrName:
                    attr = node + item
                    try:
                        #print 'attr:',attr
                        if connectionInfo(attr, isDestination=True):
                            kAttrs[attr] = {}
                        else:
                            if not self.isDefaultValue(item,getAttr(attr)):
                                nkAttrs[attr] = getAttr(attr)
                    except:
                        pass
        print 'Key Attributes:',len(kAttrs)
        #print kAttrs
        print 'Non Key Attributes:',len(nkAttrs)
        #print nkAttrs
        # 2 - Record key
        print '====== Record key ======'
        if len(kAttrs)>0:
            t = self.sTime
            while t<=self.eTime:
                currentTime(t)
                for attr in kAttrs:
                    kAttrs[attr][t] = getAttr(attr)
                t += 1
        # 2 - 1 - Optimize key
        print '====== Optimize key ======'
        dic = kAttrs.copy()
        for attr in dic.keys():
            value = dic[attr].values()
            if max(value)==min(value):# value.count(value[0]) == len(value)
                kAttrs.pop(attr)
                if not self.isDefaultValue(attr,value[0]):
                    nkAttrs[attr] = value[0]
        print 'Key Attributes:',len(kAttrs)
        #print kAttrs
        print 'Non Key Attributes:',len(nkAttrs)
        #print nkAttrs
        # Get camera - no need
        # 1 - Create dir
        if not os.path.isdir(self.cacheDir):
            os.mkdir(self.cacheDir)
        # 2 - Create new file
        name = self.cacheDir + '/' + self.valInfoName
        f = open(name,'w')
        for attr in nkAttrs.keys():
            f.write('%s %s\r\n' % (attr, nkAttrs[attr]))
        f.close()
        
        name = self.cacheDir + '/' + self.keyInfoName
        f = open(name,'w')
        for attr in kAttrs.keys():
            f.write('<attr> %s\r\n' % attr)
            for time in kAttrs[attr]:
                f.write('%s %s\r\n' % (time,kAttrs[attr][time]))
        f.close()
        self.createTime()
    def importModel(self):
        print '====== Import Model ==================='
        output = []
        # Get file list.
        name = self.cacheDir + '/' + self.refInfoName
        lines = []
        try:
            F = open(name,'r')
            lines = F.readlines()
            F.close()
        except:
            print ">>>>> Can't open file:",name
            return output
        for line in lines:
            rf = line.strip().split(' ',1)
            ns = rf[0]
            f = self.R.getFile(rf[1])
            if f != '':
                print 'Ref:',f
                output.append(file(f,r=1,namespace=ns))
            else:
                print '>>>>> No existe model:',rf
        return output
    def importCamera(self):
        print '====== Import Camera ==================='
        # Get the name camera file.
        sn = self.cacheFileName # file(q=1,sn=1,shn=1)
        cf = self.R.fileName2cameraFile(sn)
        f = self.R.getFile(cf)
        if not f=='':
            file(f,r=1,namespace='cam')
        
    def importTime(self):
        name = self.cacheDir + '/' + self.timeInfoName
        Time = []
        line = ''
        try:
            F = open(name,'r')
            line = F.readline()
            F.close()
        except:
            print ">>>>> Can't open file:",name
            return Time
        Time = line.split(' ')
        return Time
    def connectGeoCache(self):
        print '====== Import Geo Cache ===================='
        # 0 - Get time
        Time = self.importTime()
        # 1 - Get list of XML.
        xmls = os.listdir(self.geoCacheDir)
        for xml in xmls:
            print 'XML:',xml
            path = self.geoCacheDir + '/' + xml
            if os.path.isfile(path) and path.endswith('.xml'):
                lines = []
                F = open(path,'r')
                lines = F.readlines()
                F.close()
                # 2 - Get list of channl.
                # 3 - Get list of shape.
                list = {}
                for line in lines:
                    str = line.strip()
                    if ' ChannelName=' in str:
                        grp = str.split(' ')[:2]
                        #print 'grp:',grp
                        #list[grp[1][13:-1]] = grp[0][8:]
                        id = grp[0][8:]
                        name = grp[1][13:-1]
                        list[id] = [name,self.R.channelName2shapeName(name)]
                #print 'list:',list
                # 4 - Create cacheFile.
                obj = xml.split('.')[0]
                node = createNode('cacheFile',n=(obj+'_cacheFile'))
                connectAttr('time1.outTime','%s.time'%node)
                setAttr('%s.cachePath'%node,self.geoCacheDir,type="string")
                setAttr('%s.cacheName'%node,obj,type="string")
                setAttr("%s.startFrame"%node,Time[0])
                setAttr("%s.sourceStart"%node,Time[0])
                setAttr("%s.sourceEnd"%node,Time[1])
                setAttr("%s.originalStart"%node,Time[0])
                setAttr("%s.originalEnd"%node,Time[1])
                # 5 - Create switch.
                ids = list.keys()
                ids.sort()
                for id in ids:
                    channel = list[id][0] # channel0
                    shape = list[id][1] # pCylinderShape1
                    #print 'channel ID:', id
                    #print 'shape:',shape
                    # Set the channel of cacheFile node
                    setAttr('%s.channel[%s]'%(node,id),channel,type="string")
                    # Get special deformed shape
                    #if not objExists(shape):
                    shape = self.getTrueShape(shape)
                    #if objExists(shape):
                    try:
                        # Create historySwitch node
                        switch = mm.eval('createHistorySwitch("%s",false)'%shape)
                        connectAttr("%s.outCacheData[%s]"%(node,id),"%s.inp[0]"%switch,f=1)
                        connectAttr("%s.inRange"%node,"%s.playFromCache"%switch,f=1)
                    #else:
                    except:
                        print '>>>>> No exists shape:',shape
    def connectKeyCache(self):
        print 'Import Key Cache ========================='
        import string
        # Get val list
        name = self.cacheDir + '/' + self.valInfoName
        print 'Value file:',name
        lines = []
        try:
            F = open(name,'r')
            lines = F.readlines()
            #print 'lines:',lines
            F.close()
        except:
            print ">>>>> Can't open file:",name
        else:
            for line in lines:
                grp = line.strip().split(' ')
                #print 'grp:',grp
                try:
                    #print 'Set Value:',grp[0],grp[1]
                    setAttr(grp[0],string.atof(grp[1]))
                except:
                    print ">>>>> Can't sets value:",grp[0]
        # Get key list
        name1 = self.cacheDir + '/' + self.keyInfoName
        print 'key file:',name1
        lines = []
        try:
            F = open(name1,'r')
            lines = F.readlines()
            #print 'lines:',lines
            F.close()
        except:
            print ">>>>> Can't open file:",name1
        else:
            attr = ''
            ex = 0
            for line in lines:
                grp = line.strip().split(' ')
                #print 'grp:',grp
                if grp[0]=='<attr>':
                    attr = grp[1]
                    ex = objExists(attr)
                    if not ex:
                        print '>>>>> Attribute does not exist:',attr
                    continue
                else:
                    if ex:
                        try:
                            #print 'setKeyframe(%s,t=%s,v=%s)'%(attr,grp[0],grp[1])
                            setKeyframe(attr,t=string.atof(grp[0]),v=string.atof(grp[1]))
                        except:
                            print ">>>>> Can't sets key:",attr

    def createCacheFile(self):
        output = None
        print '====== Create Cache File ======================='
        rFile = []
        '''
        # 1 - Save file
        try:
            file(save=1)
        except:
            return
        '''
        # 2 - Create dir
        if not os.path.isdir(self.cacheDir):
            os.mkdir(self.cacheDir)
        # 2 - Create new file
        file(f=1,new=1)
        newFile = self.cacheDir + '/' + self.cacheFileName
        file(rename=newFile)
        try:
            output = file(f=1,s=1)
        except:
            return output
        t = self.importTime()
        currentUnit(time=self.R.timeUnit, updateAnimation=0) # ?????????????????????????
        playbackOptions(ast=float(t[0]),aet=float(t[1]))
        playbackOptions(min=float(t[0])+self.R.extTime, max=float(t[1])-self.R.extTime)
        # 3 - Ref camera
        print 'Reference camera...'
        self.importCamera()
        # 4 - Ref file
        print 'Reference file...'
        rFile = self.importModel()
        if len(rFile)==0:
            print '>>>>> No file reference...'
            return output
        # 5 - Set value
        # 6 - Set key
        self.connectKeyCache()
        # 7 - set geo cache
        print 'Set geo cache...'
        self.connectGeoCache()
        # 8 - Save file
        print 'Save file:',newFile
        file(f=1,s=1)
        return output

    def fullAction(self):
        output = None
        self.createTime()
        self.createModelList()
        self.createGeoCache()
        self.createKeyCache()
        output = self.createCacheFile()
        return output

    def do(self, action='fullAction'):
        '''
        action:
                allGeoCache - Create geo cache for all objects.
                selGeoCache - Create geo cache for selected objects.
                keyCache - Record key info and create cache file.
                setGeoCache - Import geo cache
                setKeyCache - Import key cache
                fullAction - Both creat cache and import cache.
        '''
        workflowBase.do(self)
        output = None
        
        if action == 'allGeoCache':
            self.createGeoCache()
        elif action == 'selGeoCache':
            self.createSelectedGeoCache()
        elif action == 'keyCache':
            self.createKeyCache()
        elif action == 'setGeoCache':
            self.connectGeoCache()
        elif action == 'setKeyCache':
            self.connectKeyCache()
        elif action == 'fullAction':
            output = self.fullAction()
            
        return output
# ===========================================
class updateGeoCacheUI:
    title = 'Update GeoCache - '	# Set title
    win = None
    root = None
    def __init__(self,proj):
        self.win = 'updateGeoCache_'+proj
        self.title += proj
        import ruleManager as rm
        RM = rm.ruleManager()
        RM.currentProject(proj)
        RM.currentUser('td')
        RM.currentPipeline('Dynamic')    # The string is key in pipeline.
        self.ctrl = makeCache(RM)

    def build(self):		# ( No need to change )
        if window(self.win, exists=1):
            #self.update()
            return
        window(self.win, title = self.title)
        formLayout('MAINFORM',nd=100)
        self.buildRoot()
        self.update()
        formLayout('MAINFORM',e=1,
                   af=[(self.root,'top',0),
                       (self.root,'left',0),
                       (self.root,'right',0),
                       (self.root,'bottom',0)
                       ]
                   )
        #print window(self.win,q=1,wh=1)
        window(self.win,e=1,wh=[350,400])		# Set the size of the window
    def show(self):		# ( No need to change )
        if window(self.win, exists=1):
            showWindow(self.win)
    def close(self, *args):		# ( No need to change )
        if window(self.win, exists=1):
            deleteUI(self.win)
        
    def buildRoot(self):
        self.root = frameLayout(mh=2,mw=2,lv=0,bv=0)
    def cleanup(self,root):		# ( No need to change )
        chdn = layout(root, q=1, ca=1)
        if not chdn==None:
            for chd in chdn:
                deleteUI(chd)#, layout=1
    def update(self,*args):
        self.cleanup(self.root)
        setParent(self.root)
        # build layouts
        formLayout('main',nd=100)
        button('bn',l='Update List',h=30,c=self.update)
        button('bn1',l='Update GeoCache',h=30,c=self.do)
        self.list = textScrollList('list', numberOfRows=8, allowMultiSelection=True,append=self.ctrl.refs)
        formLayout('main',e=1,
                   af=[('bn','top',2),('bn','left',2),('bn','right',2),
                       ('list','left',2),('list','right',2),
                       ('bn1','left',2),('bn1','right',2),('bn1','bottom',2)],
                   ac=[('list','top',5,'bn'),('list','bottom',5,'bn1')])
    def do(self,*args):
        self.ctrl.selectedRefs = textScrollList(self.list,q=1,si=1) # string[]
        print self.ctrl.selectedRefs
        if self.ctrl.selectedRefs==None:
            return
        self.ctrl.do('selGeoCache')
def checks():
    f = file(q=1,sn=1)
    # Checks proj
    import ruleBase as rb
    import projectsManager as pm
    r = rb.ruleBase()
    proj = r.path2projectName(f)
    p = pm.projectsManager()
    return [proj,p.isProj(proj)]
        
# Main ---------------------------------
def MakeCache(proj=''):
    if proj=='':
        v = checks()
        proj = v[0]
        if not v[1]:
            print 'No registered project:',proj
            return
    import ruleManager as rm
    RM = rm.ruleManager()
    RM.currentProject(proj)
    RM.currentUser('td')
    RM.currentPipeline('Dynamic')    # The string is key in pipeline.
    
    fn = makeCache(RM)
    return fn.do()

def makeGeoCache(proj=''): # For all refs.
    if proj=='':
        v = checks()
        proj = v[0]
        if not v[1]:
            print 'No registered project:',proj
            return
    import ruleManager as rm
    RM = rm.ruleManager()
    RM.currentProject(proj)
    RM.currentUser('td')
    RM.currentPipeline('Dynamic')    # The string is key in pipeline.
    
    fn = makeCache(RM)
    fn.do('allGeoCache')
def updateGeoCache(proj=''): # For selected refs in UI.
    if proj=='':
        v = checks()
        proj = v[0]
        if not v[1]:
            print 'No registered project:',proj
            return
    ins = updateGeoCacheUI(proj)
    #ins.close()
    ins.build()
    ins.show()
def makeKeyCache(proj=''):
    if proj=='':
        v = checks()
        proj = v[0]
        if not v[1]:
            print 'No registered project:',proj
            return
    import ruleManager as rm
    RM = rm.ruleManager()
    RM.currentProject(proj)
    RM.currentUser('td')
    RM.currentPipeline('Dynamic')    # The string is key in pipeline.
    
    fn = makeCache(RM)
    fn.do('keyCache')
def LoadGeoCache(proj='CrossFire'): # ???
    import ruleManager as rm
    RM = rm.ruleManager()
    RM.currentProject(proj)
    RM.currentUser('td')
    RM.currentPipeline('Dynamic')    # The string is key in pipeline.
    
    fn = makeCache(RM)
    fn.do('setGeoCache')
def loadKeyCache(proj=''):
    if proj=='':
        v = checks()
        proj = v[0]
        if not v[1]:
            print 'No registered project:',proj
            return
    import ruleManager as rm
    RM = rm.ruleManager()
    RM.currentProject(proj)
    RM.currentUser('td')
    RM.currentPipeline('Dynamic')    # The string is key in pipeline.
    
    fn = makeCache(RM)
    fn.do('setKeyCache')
    
# Main
#updateGeoCache()
# Batch ==================================
def BatchMakeCache():   # for CF
    path = r'\\server-03\CrossFire\3D\anim\output\AnimatonCache'
    # Get animation file list.
    all = os.listdir(path)
    print 'list:',all
    for item in all:
        if item.endswith('.mb'):
            print 'Go:',item
            import time
            info = '%s\r\n'%time.ctime()
            
            try:
                mayafile = os.path.join(path,item)
                print mayafile
                file(mayafile, o=1)
                result = MakeCache()
                info += '%s\r\n'%result
            except:
                info += '>>> %s    False\r\n'%item
            '''
            mayafile = os.path.join(path,item)
            print mayafile
            file(mayafile, f=1, o=1)
            result = MakeCache()
            info += '%s\r\n'%result
            '''
            print info
            r = recorder()
            r.append(info)
class recorder: # for CF
    path = r'\\server-03\CrossFire\3D\anim\output\AnimatonCache\History.txt'
    '''
    def read(self):
        if not os.path.isfile(self.path):
            f = open(path,'W')
            f.write('')
            f.close()
        f.open(self.path,'r')
        self.cons = f.readlines()
        f.close()
    '''
    def append(self,info):
        f = open(self.path,'r')
        orig = f.read()
        f.close()
        info += '\r\n'+orig
        f = open(self.path,'w')
        f.write(info)
        f.close()


# UI =======================================
class makeCacheUI():
    title = 'Make Cache'	# Set title
    win = None
    root = None
    win_width = 350
    win_height = 500
    def __init__(self,name):
        self.win = name
        self.checks()		# Set checks
    def checks(self):
        f = file(q=1,sn=1)
        # Checks proj
        import ruleBase as rb
        r = rb.ruleBase()
        self.proj = r.path2projectName(f)
        self.pipe = r.path2pipelineName(f)
        import projectsManager as pm
        p = pm.projectsManager()
        if p.isProj(self.proj):
            self.build()
            self.show()
        else:
            import projectsManagerUI as pmUI
            pmUI.projectEditor()

    def build(self):		# ( No need to change )
        if window(self.win, exists=1):
            self.close()
        window(self.win, title = self.title)
        formLayout('MAINFORM',nd=100)
        self.buildRoot()
        self.update()
        formLayout('MAINFORM',e=1,
                   af=[(self.root,'top',0),
                       (self.root,'left',0),
                       (self.root,'right',0),
                       (self.root,'bottom',0)
                       ]
                   )
        #print 'Last size:',window(self.win,q=1,wh=1)
        window(self.win,e=1,wh=[self.win_width,self.win_height])		# Set the size of the window
    def show(self):		# ( No need to change )
        if window(self.win, exists=1):
            showWindow(self.win)
    def close(self, *args):		# ( No need to change )
        if window(self.win, exists=1):
            deleteUI(self.win)
        
    def buildRoot(self):
        self.root = frameLayout(mh=2,mw=2,lv=0,bv=0)
    def cleanup(self,root):		# ( No need to change )
        chdn = layout(root, q=1, ca=1)
        if not chdn==None:
            for chd in chdn:
                deleteUI(chd)#, layout=1
    def update(self,*args):
        self.cleanup(self.root)
        setParent(self.root)
        # build layouts
        self.ui_1()

    def ui_1(self):
        columnLayout(adj=1)
        text(l='Current project: %s'%self.proj)
        button(l='Edit project',c=self.editProj)
        button(l='Make Cache',c=self.makeCache)
        
    def ui_2(self):
        columnLayout(adj=1)
        text(l='Unknown project file...')
        button(l='Create project',c=self.newProj)
        button(l='Edit project',c=self.editProj)
    def newProj(self,*args):
        import projectsManagerUI as pmUI
        pmUI.main()
    def editProj(self,*args):
        import projectsManagerUI as pmUI
        pmUI.main(self.proj)
    def makeCache(self,*args):
        MakeCache(self.proj)
def MakeCacheUI():
    ins = makeCacheUI('makeCache')
    #ins.close()
    ins.build()
    ins.show()