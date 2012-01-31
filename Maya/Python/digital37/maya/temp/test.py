#import pymel.core as pm
#from pymel.all import mel
#from pymel.core.general import PyNode

import logging
logger = logging.getLogger('RenderLayerPassManager') 
logger.setLevel(logging.DEBUG) 

logger.debug('a')
logger.critical('b')    
level = logger.getLevel()
print level
