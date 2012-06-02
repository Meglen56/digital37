import tempfile
import logging
import logging.handlers
import os.path
import time


class Log():
    LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
    
    def __init__(self):
        pass
            
#    def set_level(self,logLevel):
#        LOG_LEVEL = Log.LOG_LEVELS.get(logLevel)
#        logging.basicConfig(level=LOG_LEVEL)
        
    def get_file_logger(self,logDir=None,logFile=None,logLevel='debug'):
        #log = logging.getLogger("MyLogger")
        # use time.asctime() to get different logger,else will be multi-loop
        log = logging.getLogger(time.asctime())
        log.propagate = False
        
        # get tempfile's logger file if user not set
        if not logDir:
            logDir = tempfile.gettempdir()
        if not logFile:
            logFile = os.path.basename( tempfile.mkdtemp('.log', '', logDir) )

        file_log = os.path.join(logDir,logFile)
        print 'file_log:%s' % file_log
        #handler = logging.FileHandler(file_log)
        handler = logging.handlers.RotatingFileHandler(file_log, maxBytes=2097152, backupCount=5)
        handler.setLevel(Log.LOG_LEVELS.get(logLevel))
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        
#        # set maya logger handler
#        import maya.utils
#        handler = maya.utils.MayaGuiLogHandler()
#        handler.setLevel(logging.DEBUG)
#        handler.setFormatter(formatter)
#        log.addHandler(handler)
        
        return log
        
    def get_stream_logger(self):
        log = logging.getLogger("MyLogger")
        log.propagate = False
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
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
