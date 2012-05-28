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
            
        handler = logging.RotatingFileHandler(os.path.join(logDir,logFile), maxBytes=2097152, backupCount=5)
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
            s = list()
            for k, v in inputDict.iteritems() :
                s.append('key:{0}\t\nvalue{1}:\t'.format(k, v))
            self.Log.debug('\n'.join(s))
        else :
            self.Log.debug('log_dict:input is None')
    
    def log_list(self,inputList):
        if inputList :
            s = list()
            for x in inputList :
                s.append(x)
            self.Log.debug('\n'.join(s))
        else:
            self.Log.debug('log_list:input is None')

#    def write_log(self,content):
#        logPrefix = 'QC_'
#        fd,self.Log_File = tempfile.mkstemp(suffix='.log',prefix=logPrefix)
#        print self.Log_File
#        os.close(fd)
#        fObj = open(self.Log_File,'a')
#        for s in content.split('\n'):
#            fObj.write(s + '\n')
#        fObj.close()

#    def get_logger(self,logDir,name):
#        #lf = logDir.replace('\\','/') + "/logger.conf"
#        lf = os.path.abspath( logDir ).replace('\\','/') + "/logger.conf"
#        print 'lf:%s' % lf
#        f = open(lf,'r')
#        print f.read()
#        f.close()
#        logging.config.fileConfig(lf)
#        
#        print '0'
#        logger = logging.getLogger('logger'+name)
#        print '01'
#    
#        # Add file handler
#        #hdlr = logging.FileHandler( logFile )
#        #hdlr = logging.handlers.TimedRotatingFileHandler( logFile, 'midnight', 1, 5 )
#        # tell the handler to use this format
#            
#        return logger
