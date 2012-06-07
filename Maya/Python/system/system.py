import os,tempfile, subprocess, traceback
import threading
import time

class System():
    def __init__(self):
        pass
    
    def create_dir(self,dirPath):
        if not os.path.exists( dirPath ):
            try:
                os.makedirs( dirPath )
            except:
                traceback.print_exc()
                
    # user can override this function to add custom command after subprocess command complete
    def do_after_execute_cmd(self):
        self.Log.debug( 'subprocess :Success\r\n' )
        
    def set_subprocess_returnCode(self,returnCode):
        self.Subprocess_ReturnCode = returnCode
        
    def writeMessage(self,f,p):
        # set default return code
        if not self.Subprocess_ReturnCode:
            self.Subprocess_ReturnCode = [0]
            
        start_time = time.time()
        while True :
            #subprocess is not complete
            if p.poll() == None :
                if p.stdout and (time.time()-start_time<120) :
                    try:
                        output = p.stdout.readline()
                    except KeyboardInterrupt:
                        self.Log.debug( 'user canceled.\r\n' )
                        break
                    except:
                        traceback.print_exc()
                        break
                    else:
                        if output :
                            f.write( output )
                            f.flush()
            #subprocess is complete
            else :
                # some command maybe return other code than 0,so add returnCode list to match
                if p.returncode in self.Subprocess_ReturnCode:
                    self.do_after_execute_cmd()
                else:
                    self.Log.debug("ReturnCode: %s",str(p.returncode) )
                break
        
    def execute_cmd(self,cmd,logPrefix=None):
        if not logPrefix:
            logPrefix = 'temp'
        # write cmd output to log file
        fd,batch_file = tempfile.mkstemp(suffix='.bat',prefix=(logPrefix+'.'))
        os.close(fd)
        fObj = open(batch_file,'w')
        fObj.write( cmd )
        fObj.flush()
        fObj.close()
        self.Log.debug( 'execute_cmd Batch File:\t%s',batch_file )
        
        fd,log_file = tempfile.mkstemp(suffix='.log',prefix=(logPrefix+'.'))
        os.close(fd)
        self.Log.debug( 'execute_cmd log file:\t%s', log_file )
        fObj = open(log_file,'a')
        
        # For multi-line command use bat file to execute
        p = subprocess.Popen(batch_file, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        threadName = threading.Thread( target=self.writeMessage,args=( fObj,p ) )
        threadName.setDaemon(1)
        threadName.start()