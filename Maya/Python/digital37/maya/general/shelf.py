'''
Created on Jun 26, 2011

@author: Colas Fiszman
'''
import grid.path
import grid.maya.utils
import pymel.core as pm
import xml.dom.minidom
import os
import grid.maya.general.login


def loadShelfs():
    grid.maya.general.login.checkLogin()
    
    iconFolderPath = grid.path.path(os.environ.get('ICONS_PATH',None))
    
    #    get shelfTopLevel from mel command
    shelfTopLevel = pm.mel.eval('$tmpVar=$gShelfTopLevel')
    
    #    get user shelf from shelf.xml
    shelfXmlPath = grid.path.path(__file__).parent.joinpath('shelf.xml')
    
    
    if shelfXmlPath.exists() :        
        print ('Build Grid Shelf')

        #  open xml document
        shelfXml = xml.dom.minidom.parse(shelfXmlPath)
        
        #    search shelf node
        for shelf in shelfXml.getElementsByTagName('shelf'):
            
            # delete shelf if it already exist
            name = shelf.attributes["name"].value
            if pm.shelfLayout(name,exists=True) :
                pm.deleteUI(name)
            
            newShelf = pm.shelfLayout(name,p=shelfTopLevel)
            newShelf.setWidth(32)
            newShelf.setHeight(32)
            
            for button in shelf.childNodes:
                if button.nodeType == 1 :
                    cmd = button.attributes['cmd'].value
                    iconFile = button.attributes['icon'].value
                    iconPath =iconFolderPath.joinpath(iconFile)
                    annotation = button.attributes['annot'].value
                    sourceType = button.attributes['mode'].value
                    imageOverlayLabel = button.attributes['iol'].value
                    style = button.attributes['style'].value
                    
                    try :
                        # Command executed when the control is double clicked.
                        dccmd = button.attributes['dccmd'].value
                    except KeyError :
                        dccmd = None
                    if dccmd :
                        pm.shelfButton(c=cmd, image=iconPath, ann=annotation, stp=sourceType, iol=imageOverlayLabel, st=style, dcc=dccmd)
                    else :
                        pm.shelfButton(c=cmd, image=iconPath, ann=annotation, stp=sourceType, iol=imageOverlayLabel, st=style)