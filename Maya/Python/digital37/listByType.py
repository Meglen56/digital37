import os
import grid.utils
import grid.path

def listSequence(filmPath):
    '''
    Return the list of the sequence folder in filmPath.
    '''
    filmPath = grid.path.path(filmPath)
    sequenceList = filmPath.dirs(pattern='Sq*')
    sequenceList.sort()
    return sequenceList

def listShot(sequencePath):
    '''
    Return the list of the shot folder in sequencePath.
    '''
    sequencePath = grid.path.path(sequencePath)
    shotList = sequencePath.dirs(pattern='Sh*')
    shotList.sort()
    return shotList

def listShotSceneByType (shotPath, sceneType, published=False):
    shotPath = grid.path.path(shotPath)
    shotPath = shotPath.joinpath(sceneType)
    if published :
        shotPath = shotPath.joinpath('publish')
    try :
        shotSceneList = shotPath.files(pattern='*.ma')
    except WindowsError, e :
        print 'ERROR :', e
        return list() # return a empty list if a error append
    shotSceneList.sort()
    return shotSceneList
    
        
    
if __name__ == '__main__' :
    filmPath = 'H:/Streamline_Quest_Featurette_11/Film'
    for seq in listSequence(filmPath) :
        print seq
        #for shot in listShot(seq) :
            #print listShotSceneByType(shot, 'stereo', published=True)
        
#    shotPath = 'H:/Streamline_Quest_Featurette_11/Film/Sq0020/Sh0020'
#    print listShotSceneByType(shotPath, 'layout', published=True)