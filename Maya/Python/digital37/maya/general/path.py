import re

def convert_to_relative(self,parten,inputStr):
    '''
    example: convertToRelative('sourceimages','C:/AW/Maya5.0/sourceimages/maya.exe')
    result: 'sourceimages/maya.exe'
    '''
    #p = re.compile('^.*/sourceimages')
    inputStr = str(inputStr).replace('\\','/')
    returnStr = re.sub( ('^.*/(' + parten + ')'), parten, inputStr )
    print inputStr,'\t',returnStr
    return returnStr
    