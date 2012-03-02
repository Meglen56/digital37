from maya.cmds import *

class checkSameName:
    list = {}
    def check(self,onlyTransform=0):
        nodes = []
        if onlyTransform:
            nodes = ls(transforms=1)
        else:
            nodes = ls(dag=1)
        
        self.list.clear()
        for node in nodes:
            if '|' in node:
                obj = node.rsplit('|',1)[1]
                if self.list.has_key(obj):
                    self.list[obj].append(node)
                else:
                    self.list[obj] = [node]
    def showUI(self, root):
        setParent(root)
        if self.list=={}:
            text(l='There are not nodes of the same name in scene!',
                 font='boldLabelFont',align='left')
        else:
            for obj in self.list.keys():
                columnLayout(adj=1)
                iconTextButton(l=obj,h=18,style='iconAndTextHorizontal',bgc=[0.8,0.8,0.8],
                               c='from maya.cmds import *;select(%s)'%self.list[obj])
                columnLayout(adj=1,co=('left',20))
                for item in self.list[obj]:
                    iconTextButton(l=item,h=18,style='iconAndTextHorizontal',
                                   c='from maya.cmds import *;select("%s")'%item)
                setParent('..')
                setParent('..')
    def show(self):
        print self.list

class ui:
    title = 'Check Nodes Of Same Name'
    win = None
    root = None
    def __init__(self,name):
        self.win = name
    def build(self):
        if window(self.win, exists=1):
            return
        window(self.win, title = self.title,wh=(335,388))
        formLayout('main',nd=100)
        button('bn',l='Check',h=60,c=self.update)
        self.otn = checkBox('otn',v=1,l='Only Transform Nodes',align='left')
        button('bn1',l='Rename Tool',h=30,c=self.RenameTool)
        scrollLayout('scr',vst=1,hst=0,cr=1)
        self.__root()
        self.update()
        formLayout('main',e=1,
                   af=[('bn','top',5),('bn','left',2),('bn','right',2),
                       ('otn','left',20),
                       ('scr','left',2),('scr','right',2),
                       ('bn1','left',2),('bn1','right',2),('bn1','bottom',2)],
                   ac=[('otn','top',5,'bn'),('scr','top',5,'otn'),('scr','bottom',5,'bn1')])
        #print(window(self.win,q=1,wh=1)
    def __root(self):
        self.root = columnLayout(adj=1)
    def show(self):
        showWindow(self.win)
    def close(self):
        deleteUI(self.win)
    def cleanup(self):
        chd = layout(self.root, q=1, ca=1)
        if not chd==None:
            for item in chd:
                deleteUI(item)
    def update(self,*args):
        
        '''
        print( "args: " + str ( args ) )
        '''
        otn = checkBox(self.otn,q=1,v=1)
        csn = checkSameName()
        csn.check(otn)
        self.cleanup()
        csn.showUI(self.root)
        '''
        setParent(self.root)
        if csn.list=={}:
            text(l='There are not nodes of the same name in scene!',
                 font='boldLabelFont',align='left')
        else:
            for obj in csn.list.keys():
                columnLayout(adj=1)
                iconTextButton(l=obj,h=18,style='iconAndTextHorizontal',
                               c='from maya.cmds import *;select(%s)'%csn.list[obj])
                columnLayout(adj=1,co=('left',12))
                for item in csn.list[obj]:
                    iconTextButton(l=item,h=18,style='iconAndTextHorizontal',
                                   c='from maya.cmds import *;select("%s")'%item)
                setParent('..')
                setParent('..')
        '''
    def RenameTool(self,*args):
        import App.maya.projectFlow.nameCtrl as nc
        nc.nodeNameManager()

def CheckSameName():
    win = ui('CheckSameName')
    win.build()
    win.show()
'''        
csn = checkSameName()
csn.check()
csn.show()
'''