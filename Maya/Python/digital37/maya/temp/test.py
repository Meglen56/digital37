#import pymel.core as pm
#from pymel.all import mel
#from pymel.core.general import PyNode

import logging
LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
              'warning': logging.WARNING, 'error': logging.ERROR,\
              'critical': logging.CRITICAL}
LOG_LEVEL = LOG_LEVELS.get('warning')
#logging.basicConfig(level=LOG_LEVEL)
logging.debug('a')
logging.critical('b')    

