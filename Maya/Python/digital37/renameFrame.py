import os

import grid.path

import listByType


def renameFrame (filmPath):
    for seq in listByType.listSequence(filmPath)[4:]:
        print seq
        for shot in listByType.listShot(seq) :
            try :
                print shot
                shotDirPath = grid.path.path (shot)
                playblastDir = shotDirPath.joinpath('stereo','publish','Playblast')
                leftDirPath = playblastDir.joinpath('Left')
                rightDirPath = playblastDir.joinpath('Right')
                for frame in leftDirPath.files() :
                    nameList = frame.split('.')
                    newName = '%s_left.%s.%s'%(nameList[0],nameList[1],nameList[2])
                    os.rename(frame, newName)
                for frame in rightDirPath.files() :
                    nameList = frame.split('.')
                    newName = '%s_right.%s.%s'%(nameList[0],nameList[1],nameList[2])
                    os.rename(frame, newName)
            except :
                print 'ERROR :', shot
                
if __name__ == '__main__' :
    filmPath = 'H:/Streamline_Quest_Featurette_11/Film'
    renameFrame(filmPath)
    
