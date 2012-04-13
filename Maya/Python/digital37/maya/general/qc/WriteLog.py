#coding=gbk
'''
logging level:
Numeric value
CRITICAL 50
ERROR    40
WARNING  30
INFO     20
DEBUG    10
NOTSET   0
'''
import logging,logging.config,os

LogFile = None

def log(etcFolder,name):
    lf = os.path.abspath( etcFolder + "/config" ).replace('\\','/') + "/logger.conf"
    #print 'lf:%s',lf
    logging.config.fileConfig(lf)

    logger = logging.getLogger('logger'+name)

    # Add file handler
    #hdlr = logging.FileHandler( logFile )
    #hdlr = logging.handlers.TimedRotatingFileHandler( logFile, 'midnight', 1, 5 )
    # tell the handler to use this format
        
    return logger
