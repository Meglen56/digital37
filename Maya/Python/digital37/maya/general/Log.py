import tempfile, subprocess, traceback
import logging
import os

class Log():
    def __init__(self):
        self.Log = self.get_stream_logger()
            
    def setLog(self,logLevel):
        LOG_LEVELS = {'debug': logging.DEBUG, 'info':logging.INFO, \
                  'warning': logging.WARNING, 'error': logging.ERROR,\
                  'critical': logging.CRITICAL}
        LOG_LEVEL = LOG_LEVELS.get(logLevel)
        logging.basicConfig(level=LOG_LEVEL)
        
    def get_file_logger(self,etcFolder,name):
        log = logging.getLogger("MyLogger")
        log.propagate = False
        #handler = logging.RotatingFileHandler
        handler = logging.FileHandler(etcFolder+ "/" + name)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        return log
        
    def get_stream_logger(self):
        log = logging.getLogger("MyLogger")
        log.propagate = False
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        return log
                    
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