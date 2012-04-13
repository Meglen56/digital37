import tempfile, subprocess, traceback
import logging
import os

class Log():
    def __init__(self):
        pass
            
    def setLog(self,logLevel):
        LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
        LOG_LEVEL = LOG_LEVELS.get(logLevel)
        logging.basicConfig(level=LOG_LEVEL)
        
    def get_logger(self,etcFolder,name):
        log = logging.getLogger("MyLogger")
        log.propagate = False
        #handler = logging.RotatingFileHandler
        handler = logging.FileHandler(etcFolder+ "/qc.log")
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
                
    def log_dict(self,inputDict):
        if inputDict :
            s = ''
            try :
                s += str(inputDict)
            except :
                self.Log.warning('can not convert inputDict to string')        
            for k,v in inputDict.items() :
                s += '\t\t'
                s += 'key:'+str(k) + '\t'
                s += 'value:'+str(v)
            self.Log.debug(s)
    
    def log_list(self,inputList):
        if inputList :
            s = ''
            if inputList :
                try :
                    s += str(inputList)
                except :
                    self.Log.warning('can not convert inputList to string')
                for i in inputList :
                    s += '\t' + str(i)
            self.Log.debug(s)
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

#    def get_logger(self,etcFolder,name):
#        #lf = etcFolder.replace('\\','/') + "/logger.conf"
#        lf = os.path.abspath( etcFolder ).replace('\\','/') + "/logger.conf"
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