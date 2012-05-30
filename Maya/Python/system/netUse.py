import os

def netUse():
    cmd =r'NET USE V: \\SERVER-03\37artists\mhxy \\ /YES'
    os.system(cmd)
    
netUse()