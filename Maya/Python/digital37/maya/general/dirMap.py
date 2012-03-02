import maya.cmds as cmds

def dirMap(mapDict):
    cmds.dirmap( en=True )
    for k,v in mapDict.iteritems() :
        cmds.dirmap( m=(k, v) )
    #cmds.dirmap( cd='/usr/maya/textures/characters/skin1.iff' )

def __main__(mapDict):
    print 'dirMap'
    dirMap(mapDict)
    # add '/' at the end
    print cmds.dirmap( cd='d:/mhxy//sourceimages/' )
    print cmds.dirmap( cd='d:/mhxy/sourceimages/' )
    print cmds.dirmap( cd='/sourceimages/' )
    
if __name__ == '__main__':
    #__main__({'d:\\mhxy\\sourceimages':'Q:/data','d:/mhxy/scenes':'Q:/data'})
    __main__({'/sourceimages':'Q:/mhxy/sourceimages',\
              'd:/mhxy/sourceimages':'Q:/mhxy/sourceimages',\
              'D:/mhxy/sourceimages':'Q:/mhxy/sourceimages',\
              'd:/mhxy//sourceimages':'Q:/mhxy/sourceimages',\
              'D:/mhxy//sourceimages':'Q:/mhxy/sourceimages'})
    
#__main__({'d:/mhxy/sourceimages':'Q:/data'})