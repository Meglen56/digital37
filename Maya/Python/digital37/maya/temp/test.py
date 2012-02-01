import pymel.core as pm
from pymel.all import mel
from pymel.core.general import PyNode

light_set = set()
mel.eval('SelectAllLights')
light_set.update( pm.ls(sl=1,l=1) )
light_set.update( pm.ls(sl=1,l=1,dag=1,lf=1,\
                        type=['spotLight','directionalLight',\
                        'volumeLight','areaLight','ambientLight','pointLight']) )
print light_set
return light_set



