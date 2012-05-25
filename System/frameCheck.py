#!/usr/bin/env python
#Description:check frame 
#Author:honglou(hongloull@hotmail.com)
#Create:2008.08.27
#Update:2008.09.09
#How to use :
import os.path
import sys
import re
import glob
import string
import logging

# Get file lists from folder
def getFileFromDir(fileName,inputPad):
	noPad = 0
	imageName = ''
	# "layer1/beauty.%4n.iff"
	p = re.compile(r'%[0-9]{1,1}n')
	imageName = re.sub( p, '*', fileName )
	
	logging.debug('imageName:%s',imageName)

	p = re.compile(r'%[0-9]{1,1}n')
	try:
		pad = p.search(fileName).group()
		p = re.compile(r'[0-9]{1,1}')
		pad = p.search(pad).group()
	# For no %n
	except:
		pad = inputPad
		noPad = 1
		imageName = fileName + '.*'
		
	returnList = []
	for f in glob.glob(imageName):
		returnList.append( os.path.normpath( f ) )
		
	return [returnList,pad,noPad]
	
def frameCheck(fileName,inputPad,frames):
	error = {}
	errorFrame = ''

	# Get parent folder
	p = re.compile('^.*/')
	folder = p.search(fileName).group()
	
	p = re.compile(r'%[0-9]{1,1}n')

	logging.debug('fileName:%s',fileName)
	
	# For dir exists
	if os.path.exists(folder):
		fileLists,pad,noPad = getFileFromDir(fileName,inputPad)
		## for f in fileLists:
## 			logging.debug('fileLists:%s',f)

		for frame in frames :
			logging.debug('frame:%s',frame)
			if frame != '' :
				if noPad == 0 :
					# replace %4n with 0001
					f = re.sub( p, string.zfill(frame,int(pad)), fileName )
				else :
					f = fileName + '.' + string.zfill(frame,int(pad))

				f = os.path.normpath( f )
				logging.debug('f:%s',f)
				if f not in fileLists :
					errorFrame += frame + ' '
			
	# For dir not exists
	else:
		errorFrame = ' '.join( frames )

	error['folder'] = folder
	if errorFrame:
		error['frames'] = errorFrame
	print 'error:',error
	return error
			
if __name__=='__main__':
	#frameCheck('/mnt/rnd/NetRender/pySource/project/mayaProject/images','test','4','iff',[1,2,3,4,5,6,7,8,9,10,1001])
	frameCheck('Z:\D031SEER\sequence\ep02\ep02_sc0020\output','seer_an_ep02_sc0020','3','tif','1-1000')
