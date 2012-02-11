#coding=gbk
# -*- coding:utf-8 -*-
import traceback

import xml.etree.ElementTree as ET

class XmlParser:
    def __init__(self,inputData):
        self.tree = None
        inputData = inputData.encode('utf-8')
        try:
            self.tree = ET.XML( inputData )
        except:
            traceback.print_exc()

    def getElementKey(self,name):
        #print self.tree.getroot( )
        for parent in self.tree.getiterator( name ):
            #print parent
            if parent.keys():
                #print parent.keys()
                outputData = parent.keys()
        #print outputData
        return outputData
    
    def getItemsTag(self):
        outputList = []
        if self.tree != None :
            for parent in self.tree.getiterator():
                outputList.append( parent.tag )
        return outputList
    
    def getAttr2(self,keyName,inputKey):
        outputStr = None
        if self.tree != None :
            for parent in self.tree.getiterator(tag=keyName):
                outputStr = parent.attrib.get( inputKey )
        #print 'outputDict:%s' % outputDict
        return outputStr
    
    def getAttr3(self,keyName,inputKey):
        outputStr = []
        if self.tree != None :
            for parent in self.tree.getiterator(tag=keyName):
                outputStr.append( parent.attrib.get( inputKey ) )
        #print 'outputDict:%s' % outputDict
        return outputStr
    
    def getAttr(self,keyName,inputKey,inputValue,inputKey2):
        outputStr = None
        isBreak = 0
        if self.tree != None :
            for parent in self.tree.getiterator(tag=keyName):
                if isBreak == 0 :
                    if parent.attrib.get( inputKey ) == inputValue :
                        outputStr = parent.attrib.get( inputKey2 )
                        isBreak = 1
        #print 'outputDict:%s' % outputDict
        return outputStr
    
    def getAttrs(self,keyName,inputKey,inputValue,inputKey2):
        outputList = []
        if self.tree != None :
            for parent in self.tree.getiterator(tag=keyName):
                if parent.attrib.get( inputKey ) == inputValue :
                    outputList.append( parent.attrib.get( inputKey2 ) )
        #print 'outputDict:%s' % outputDict
        return outputList
    
    def getListByKey(self,keyName):
        outputList = []
        if self.tree != None :
            for parent in self.tree.getiterator(tag=keyName):
                # Remove empty items
                if parent.items() != []:
                    #print 'parent.items:',parent.items()
                    #print 'parent.tag:',parent.tag
                    d = {}
                    for k,v in parent.items():
                        d[k] = v
                    outputList.append(d)
        #print 'outputDict:%s' % outputDict
        return outputList
        
    def getItemsByKey(self,keyName):
        outputDict = {}
        if self.tree != None :
            for parent in self.tree.getiterator():
                # Remove empty items
                if parent.items() != []:
                    #print 'parent.items:',parent.items()
                    #print 'parent.tag:',parent.tag
                    if parent.tag == keyName :
                        #print 'parent.tag:',parent.tag
                        #print 'parent.items:',parent.items()
                        d = {}
                        for k,v in parent.items():
                            d[k] = v
                        outputDict[parent.tag] = d
                    else :
                        pass
        #print 'outputDict:%s' % outputDict
        return outputDict
    
    def getItems(self):
        outputDict = {}
        if self.tree != None :
            #outputData = dict((c, p) for p in self.tree.getiterator() for c in p)
            for parent in self.tree.getiterator():
                # Remove empty items
                if parent.items() != []:
                    #print parent.tag
                    #print parent.items()
                    d = {}
                    for k,v in parent.items():
                        d[k] = v
                    outputDict[parent.tag] = d
        #print 'outputDict:%s' % outputDict
        return outputDict
    
    def getRoot(self):
        if self.tree != None :
            for parent in self.tree.getiterator( ):
                #print parent
                if parent.keys():
                    #print parent.keys()
                    outputData = parent.keys()
            #print outputData
        return outputData
    
    def getElementItemsByKey(self,name,keyName):
        outputData = {}
        #print 'self.tree:%s' % self.tree
        if self.tree != None :
            #print '*'
            client = {}
            for parent in self.tree.getiterator( name ):
                #print 'parent:',parent
                for key,value in parent.items():
                    #print 'key:',key
                    #print 'value:',value
                    if key == keyName :
                        client = value
                        #print 'type:',type(client)
                outputData.setdefault( parent.get(keyName),client )
        return client
    
    def getElementItems(self,name,keyName):
        outputData = {}
        #print 'self.tree:%s' % self.tree
        if self.tree != None :
            #print '*'
            for parent in self.tree.getiterator( name ):
                #print 'parent:',parent.items()
                client = {}
                for k,v in parent.items():
                    client.setdefault( k,v )
                if parent.text :
                    client.setdefault('note',parent.text)  
                outputData.setdefault( parent.get(keyName),client )
        return outputData  

    # Only for system_complex model
    def getElementItemsForShell(self,name,keyName):
        outputData = {}
        
        #print 'self.tree:%s' % self.tree
        if self.tree != None :
            #print '*'
            tmp = []
            for parent in self.tree.getiterator( name ):
                #print 'parent:',parent.items()
                client = {}
                for k,v in parent.items():
                    isMatch = 0
                    if k == keyName :
                        if v == parent.get(keyName) :
                            isMatch = 1
                    if isMatch == 1 :
                        client.setdefault( k,v )

                #print 'parent.get(keyName):',parent.get(keyName)
                #print 'client:',client
                
                #print 'outputData:',outputData
                if not outputData.has_key( parent.get(keyName) ) :
                    tmp = [client]
                else :
                    tmp.append( client )

                #print 'tmp:',tmp
                    
                outputData[parent.get(keyName)] = tmp
                #print 'outputData:',outputData
        #print 'outputData final:',outputData
        return outputData
    
    def getElementItems2(self,name,keyName,subElement='subElement'):
        outputData = {}
        #print 'self.tree:%s' % self.tree
        if self.tree != None :
            #print self.tree.getroot()
            for parent in self.tree.getiterator( name ):
                #print parent
                client = {}
                for key,value in parent.items():
                    client.setdefault( key,value )
                if parent.text :
                    i = 0
                    for c in parent.getchildren() :
                        d = {}
                        for k1,v1 in c.items() :
                            d[k1] = v1
                        i += 1
                        client.setdefault((subElement + str(i)),d)
                    #print 'parent.text:%s' % parent.text
                outputData.setdefault( parent.get(keyName),client )
        return outputData 
    
class MakeXml:
    def __init__(self):
        pass
        
##     def createElement(self,root,inputData=None,subRoot=None,subElementData=None,subRoot1=None,subElementData1=None):
##         elem = ET.Element( root )
##         for key,value in inputData.items():
##             elem.attrib[key] = value
            
##         if subRoot:
##             subDict = {}
##             for key,value in subElementData.items() :
##                 subElem = ET.SubElement( elem, subRoot )
##                 for key,value in value.items():
##                     subElem.attrib[key] = value
                    
##         if subRoot1:
##             subDict = {}
##             for key,value in subElementData1.items() :
##                 subElem = ET.SubElement( elem, subRoot1 )
##                 subElem.attrib[key] = value
##         #print ET.tostring( elem )
##         #ET.dump( elem )
##         return ET.tostring( elem )
    
    def createElement(self,root,inputData=None,subRoot=None,subElementData=None,subRoot1=None,subElementData1=None):
        elem = ET.Element( root )
        for key,value in inputData.items():
            elem.attrib[key] = value
            
        if subRoot:
            # If is dict, then loop 
##             if type(subElementData) == type([]) :
##                 for s in subElementData :
##                     subDict = {}
##                     for key,value in s.items() :
##                         subElem = ET.SubElement( elem, subRoot )
##                         for key,value in value.items():
##                             subElem.attrib[key] = value
##             else :
            tmp = {}
            for key,value in subElementData.items() :
                #subElem = ET.SubElement( elem, subRoot )
                for v in value.itervalues():
                    if type(v) == type([]) :
                        tmp[key] = v

            #print 'tmp:',tmp
            if tmp == {} :
                for key,value in subElementData.items() :
                    subElem = ET.SubElement( elem, subRoot )
                    for key,value in value.items():
                        if type(value) != type([]) :
                            subElem.attrib[key] = value
                        else :
                            tmp = value
                        
            else :
                for k2,v2 in tmp.items() :
                    #print 'k2:%s v2:%s' % (k2,v2)
                    for l in v2 :
                        subElem = ET.SubElement( elem, subRoot )
                        for key,value in subElementData[k2].items() :
                            #print 'key:%s value:%s' % (key,value)
                            if type(value) != type([]) :
                                subElem.attrib[key] = value
                            else :
                                subElem.attrib[key] = l
                                    
        if subRoot1:
            for key,value in subElementData1.items() :
                subElem = ET.SubElement( elem, subRoot1 )
                subElem.attrib[key] = value
        #print ET.tostring( elem )
        #ET.dump( elem )
        return ET.tostring( elem )
    
    def createElements(self,root,inputData,subElementData=None):
        elem = ET.Element( root )
        if inputData : 
            for key,value in inputData.items():
                print 'key:',key
                print 'value:',value
                if type(value) == type(''):
                    elem.attrib[key] = value
                elif type(value) == type(set()) or type(value) == type(list()) :
                    for i in value:
                        print i
                        elem.attrib[key] = i
                else:
                    print type(value)
        if subElementData :
            for key,value in subElementData.items() :
                subElem = ET.SubElement( elem, key )
                for v in value:
                    #print 'v:%s' % v 
                    #subElem.attrib[v] = v
                    ET.SubElement(subElem, v)
        return ET.tostring( elem )
    
    def createElements2(self,root,inputData,subElementData=None):
        elem = ET.Element( root )
        if inputData :
            for key,value in inputData.items():
                elem.attrib[key] = value
            
        if subElementData :
            for k,v in subElementData.items() :
                subElem = ET.SubElement( elem, k )
                for k1,v1 in v.items() :
                    subElem.attrib[k1] = v1
        return ET.tostring( elem )
    
    def createElements3(self,root,inputData,subElementData=None):
        elem = ET.Element( root )
        if inputData :
            for key,value in inputData.items():
                elem.attrib[key] = value
            
        if subElementData :
            for k,v in subElementData.items() :
                subElem = ET.SubElement( elem, k )
                for k1,v1 in v.items() :
                    if type(v1) == type({}):
                        subElem2 = ET.SubElement( subElem, k1 )
                        for k2,v2 in v1.items():
                            subElem2.attrib[k2] = v2
                    else :
                        subElem.attrib[k1] = v1
        return ET.tostring( elem )
    
if __name__ == '__main__':    
    inputData = '<?xml version="1.0" encoding="UTF-8"?><Event time="2009-07-24 10:05:20" Message="test74: -e 8  -s 7  finish." user="Service" ip="192.168.20.133" machine="ASPLNX049" type="Finish" />'
    xP = XmlParser( inputData )
    # get client key from xml
    #CommandmodelKey = xP.getElementKey('Quest')
##     CommandmodelItems = xP.getRoot( )
##     print 'Commandmodel:' % CommandmodelItems
    # get client items from xml

    CommandmodelItems = xP.getElementItems( 'Event','time' )
