import os.path

def create_dir(self,dirPath):
    if not os.path.exists( dirPath ):
        os.makedirs( dirPath )
        
def __main__():
    create_dir('d:/temp/deadline')