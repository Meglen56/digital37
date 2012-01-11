import sys
import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI

# Make MRRenderLayerPassUI by: pyuic4 MRRenderLayerPass.ui>MRRenderLayerPassUI.py
import digital37.maya.lighting.MRRenderLayerPassUI 
# reload only for tests
reload(digital37.maya.lighting.MRRenderLayerPassUI)

import digital37.maya.lighting.MRRenderLayerPass
# reload only for tests 
reload(digital37.maya.lighting.MRRenderLayerPass)

class StartMRRenderLayerPass(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = digital37.maya.lighting.MRRenderLayerPassUI.Ui_root()
        self.ui.setupUi(self)
        self.renderLayer =  digital37.maya.lighting.MRRenderLayerPass.MRRenderLayerPass()
        self.material =  digital37.maya.lighting.MRRenderLayerPass.MRMaterial()
        self.initColorLayer()
        #
       
    def on_listWidget_assignedPasses_dragEnterEvent(self,event):
        print 'dragEnter'
        event.acceptProposedAction()
#            
#    def on_listWidget_assignedPasses_dragMoveEvent(self,event):
#        print 'dragMove'
#        event.acceptProposedAction()
#        
#    def on_listWidget_assignedPasses_dropEvent(self,event):
#        print 'dropEvent'
#        event.accept()
        
    def initColorLayer(self):
        #self.renderLayer.PASSES
        listItem1 = []
        for lst in self.renderLayer.PASSES_COLOR:
            listItem1.append(QtGui.QListWidgetItem(lst))
        for i in range(len(listItem1)):
            self.ui.listWidget_assignedPasses.insertItem(i+1,listItem1[i])
        listItem2 = []
        for lst in self.renderLayer.PASSES_COLOR_AVAILABLE:
            listItem2.append(QtGui.QListWidgetItem(lst))
        for i in range(len(listItem2)):
            self.ui.listWidget_availablePasses.insertItem(i+1,listItem2[i])
            
    def getColorLayerValue(self):
        self.renderLayer.LAYER_NAME = str( self.ui.lineEdit_color_layerName.text() )
        self.renderLayer.PREFIX_PASS = str( self.ui.lineEdit_color_passPrefix.text() )
        self.renderLayer.SUFFIX_PASS = str( self.ui.lineEdit_color_passSuffix.text() )        
        self.renderLayer.PASSES_COLOR = []
        for i in range(self.ui.listWidget_assignedPasses.count()) :
            self.renderLayer.PASSES_COLOR.append( str( self.ui.listWidget_assignedPasses.item(i).text() ) )

    def getAOLayerValue(self):
        self.renderLayer.LAYER_NAME = str( self.ui.lineEdit_ao_layerName.text() )
        self.renderLayer.PREFIX_PASS = str( self.ui.lineEdit_ao_passPrefix.text() )
        self.renderLayer.SUFFIX_PASS = str( self.ui.lineEdit_ao_passSuffix.text() )
        
    def on_pushButton_ao_apply_pressed(self):
        self.getAOLayerValue()
        isTransparency = self.ui.radioButton_ao_transparency.isChecked()
        #isTransparency = False
        isAddPass = self.ui.checkBox_addAoPass.isChecked()
        #isAddPass = False
        if not isTransparency :
            self.renderLayer.createAOLayer( isAddPass )
        else :
            self.renderLayer.createAOTransparencyLayer( isAddPass )
                        
    def on_pushButton_CRL_aO_pressed(self):
        self.renderLayer.createAOLayer()
        
    def on_pushButton_color_apply_pressed(self):
        self.getColorLayerValue()
        self.renderLayer.createColorLayer()
        
    def on_pushButton_CRL_keyLight_pressed(self):
        self.renderLayer.createLightLayer('key',[0,1,0])        

    def on_pushButton_CRL_fillLight_pressed(self):
        self.renderLayer.createLightLayer('fill',[1,0,0])
        
    def on_pushButton_CRL_backLight_pressed(self):
        self.renderLayer.createLightLayer('back',[0,0,1])
        
    def on_pushButton_CRL_shadow_pressed(self):
        self.renderLayer.createShadowLayer('black')
        
    def on_pushButton_CM_black_pressed(self):
        #self.material.createShader([0,0,0],[1,1,1],'BLACK_MATTE')
        print 'black'
        
    def on_pushButton_CM_blackNoAlpha_pressed(self):
        self.material.createShader([0,0,0],[0,0,0],'BLACK_NO_ALPHA_MATTE')
                                        
    def on_pushButton_CM_red_pressed(self):
        self.material.createShader([1,0,0],[1,1,1],'RED_MATTE')
                                        
    def on_pushButton_CM_green_pressed(self):
        self.material.createShader([0,1,0],[1,1,1],'GREEN_MATTE')
                                        
    def on_pushButton_CM_blue_pressed(self):
        self.material.createShader([0,0,1],[1,1,1],'BLUE_MATTE')
                                        
    def on_pushButton_CM_useBackground_pressed(self):
        self.material.createShadowShader('userBackGround',None,1)
                                        
    def on_pushButton_CM_zDepth_pressed(self):
        self.material.createZDepthShader('Z_Depth_MAT')
                                                                                
    def on_pushButton_RS_apply_pressed(self):
        #Get widget status
        #Define a dict
        renderStatus = {'castsShadows':[self.ui.checkBox_castsShadows,1],\
                        'receiveShadows':[self.ui.checkBox_receiveShadows,1],\
                        'motionBlur':[self.ui.checkBox_motionBlur,1],\
                        'primaryVisibility':[self.ui.checkBox_primaryVisibility,1],\
                        'smoothShading':[self.ui.checkBox_smoothShading,1],\
                        'visibleInReflections':[self.ui.checkBox_visibleInReflections,1],\
                        'visibleInRefractions':[self.ui.checkBox_visibleInRefractions,1],\
                        'doubleSided':[self.ui.checkBox_doubleSided,1],\
                        'opposite':[self.ui.checkBox_opposite,1]
                        }
        for k,v in renderStatus.items() :
            v[1] = v[0].isChecked()
        digital37.maya.lighting.MRRenderLayerPass.setRenderStatus( renderStatus )
                
def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def main():
    global MRRenderLayerPass_app
    global MRRenderLayerPass_myapp
    MRRenderLayerPass_app = QtGui.qApp
    MRRenderLayerPass_myapp = StartMRRenderLayerPass(getMayaWindow())
    MRRenderLayerPass_myapp.show()
        
if __name__ == "__main__":
    main()

