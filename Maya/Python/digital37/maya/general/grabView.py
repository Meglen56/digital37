import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import pymel.core as pm
import time

def set_attr_for_pb(cameraShape):
    '''set camera attributes for playblast
    '''
    pm.camera(cameraShape,e=1,displayFilmGate=0,displayResolution=0,displaySafeAction=0,overscan=1.0)
    
def get_current_cam():
    return pm.ls(sl=1,dag=1,lf=1,type='camera')[0]
    
class GrabView():
    '''
    grab the frame buffer from the active viewport (You could also change 
    it to be a specified viewport with little work) and write it to any 
    format that MImage supports
    '''
    def __init__(self):
        pass
    
    def grab_view(self,imageName):
        #Grab the last active 3d viewport
        view = apiUI.M3dView.active3dView()
        #read the color buffer from the view, and save the MImage to disk
        image = api.MImage()
        view.readColorBuffer(image, True)
        image.writeToFile(imageName, 'jpg')
        view.refresh(True,True)
        
    def main(self,imagePath):
        # get camera
        cam = get_current_cam()
        set_attr_for_pb(cam)
        imageName = '%s/%s' % (imagePath,cam.name())
        # grab image
        # get current time
        min_time = int(pm.playbackOptions( q=True,minTime=True )) 
        max_time = int(pm.playbackOptions( q=True,maxTime=True )) + 1
        for i in range(min_time,max_time):
            pm.currentTime(i,e=1,update=1)
            pm.refresh(f=1)
            #panel = pm.paneLayout('viewPanes', q=True, pane1=True)
            #pm.isolateSelect(panel,state=1)
            #pm.isolateSelect(panel,state=0)
            #self.grab_view( '%s.%s.jpg' % (imageName,i) )
            self.grab_view( '%s.%s.jpg' % (imageName,i) )
            
def main():
    GrabView().main('d:/test')
        
