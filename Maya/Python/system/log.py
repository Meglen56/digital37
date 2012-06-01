import tempfile
import logging
import os.path

class Log():
    def __init__(self):
        pass
            
    def setLog(self,logLevel):
        LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
        LOG_LEVEL = LOG_LEVELS.get(logLevel)
        logging.basicConfig(level=LOG_LEVEL)
        
    def get_logger(self,logDir=None,logFile=None):
        log = logging.getLogger("MyLogger")
        log.propagate = False
        
        # get tempfile's logger file if user not set
        if not logDir:
            logDir = tempfile.gettempdir()
        if not logFile:
            logFile = os.path.basename( tempfile.mkdtemp('.log', '', logDir) )
        
        #handler = logging.FileHandler(os.path.join(logDir,logFile), maxBytes=2097152, backupCount=5)
        handler = logging.FileHandler(os.path.join(logDir,logFile))
        #handler = logging.FileHandler(logDir+ "/qc.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        
        return log
    
#    def setLog_maya(self):
#        self.Log = logging.getLogger("MyLogger")
#        self.Log.propagate = False
#        handler = maya.utils.MayaGuiLogHandler()
#        handler.setLevel(logging.DEBUG)
#        formatter = logging.Formatter("%(asctime)s %(message)s")
#        handler.setFormatter(formatter)
#        self.Log.addHandler(handler)
                
    def log_dict(self, inputDict):
        if inputDict :
            self.Log.debug( '\n'.join( [ 'key:{0}\t\nvalue{1}:\t'.format(k, v) for k, v in inputDict.iteritems() ] ) )
        else :
            self.Log.debug('log_dict:input is None')
    
    def log_list(self,inputList):
        if inputList :
            self.Log.debug( '\n'.join( [ x for x in inputList] ) )
        else:
            self.Log.debug('log_list:input is None')
