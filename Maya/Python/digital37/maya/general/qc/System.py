import os,tempfile, subprocess, traceback
import threading

class System():
    def __init__(self):
        pass
    
    def writeMessage(self,f,p):
        while True :
            #subprocess is not complete
            if p.poll() == None :
                if p.stdout :
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
                if(p.returncode==0):
                    self.Log.debug( 'QC:Success\r\n' )
                else:
                    self.Log.debug("ReturnCode: %s",str(p.returncode) )
                break
        
    def execute_cmd(self,cmd,logPrefix):
        # write cmd output to log file
        fd,batch_file = tempfile.mkstemp(suffix='.bat',prefix=('.'+logPrefix))
        os.close(fd)
        fObj = open(batch_file,'w')
        fObj.write( cmd )
        fObj.flush()
        fObj.close()
        self.Log.debug( 'Batch File:\t%s',batch_file )
        
        fd,self.Log = tempfile.mkstemp(suffix='.log',prefix=('.'+logPrefix))
        os.close(fd)
        fObj = open(self.Log,'a')
        
        # For multi-line command use bat file to execute
        p = subprocess.Popen(batch_file, shell=True, bufsize=512,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        threadName = threading.Thread( target=self.writeMessage,args=( fObj,p ) )
        threadName.setDaemon(1)
        threadName.start()