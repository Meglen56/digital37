import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import traceback

# Load mental ray plugin first, else can not made some global var	  
def load_plugin():
	#Check MR plugin load or not
	import digital37.maya.general.plugin as plugin
	reload(plugin)
	plugin.load_plugin('Mayatomr')

# Let maya make some mr attr
def set_renderer_to_mentalray(): 
	DEFAULT_RENDER_GLOBALS = pm.PyNode('defaultRenderGlobals')
	renderer = DEFAULT_RENDER_GLOBALS.currentRenderer.get()
	if renderer != 'mentalRay' :
		DEFAULT_RENDER_GLOBALS.currentRenderer.set('mentalRay')
		
def init_mentalray(log=None):
	'''
	initialize mentalray 
	'''
	load_plugin()
	
	if not log:
		import logging
		log = logging.getLogger()
		
	create_mentalray_nodes(log)
	set_renderer_to_mentalray()
	
def create_mentalray_nodes(log=None):
	'''
	create mentalray nodes
	'''
	try:
		pm.PyNode('defaultRenderGlobals')
	except:
		log.warning('Get defaultRenderGlobals error.')
		pm.createNode('defaultRenderGlobals')
	
	try:
		pm.PyNode('mentalrayGlobals')
	except:
		log.warning('Get mentalrayGlobals error.')
		try:
			mel.eval('miCreateDefaultNodes')
		except:
			log.error(traceback.format_exc())
			
	try:
		pm.PyNode('miDefaultOptions')
	except:
		log.warning('Get miDefaultOptions error.')
		try:
			mel.eval('miCreateDefaultNodes')
		except:
			log.error(traceback.format_exc())
		
	try:
		pm.PyNode('miDefaultFramebuffer')
	except:
		log.warning('Get miDefaultFramebuffer error.')
		try:
			mel.eval('miCreateDefaultNodes')
		except:
			log.error(traceback.format_exc())
	
	try:
		pm.PyNode('mentalrayItemsList')
	except:
		log.warning('Get mentalrayItemsList error.')
		try:
			mel.eval('miCreateDefaultNodes')
		except:
			log.error(traceback.format_exc())
	
#=======================================================================
# if not self.MENTAL_RAY_GLOBALS.options in self.MI_DEFAULT_OPTIONS.message.listConnections(d=1,p=1) :
#	try:
#		self.MI_DEFAULT_OPTIONS.message.connect( self.MENTAL_RAY_GLOBALS.options )
#	except:
#		log.error(traceback.format_exc())
# 
# if not self.MENTAL_RAY_GLOBALS.framebuffer in self.MI_DEFAULT_FRAME_BUFFER.message.listConnections(d=1,p=1) :
#	try:
#		self.MI_DEFAULT_FRAME_BUFFER.message.connect( self.MENTAL_RAY_GLOBALS.framebuffer )
#	except:
#		log.error(traceback.format_exc())
#  
# if not self.MENTAL_RAY_ITEMS_LIST.globals in self.MENTAL_RAY_GLOBALS.message.listConnections(d=1,p=1) :  
#	try:
#		self.MENTAL_RAY_GLOBALS.message.connect( self.MENTAL_RAY_ITEMS_LIST.globals )
#	except:
#		log.error(traceback.format_exc())
#=======================================================================