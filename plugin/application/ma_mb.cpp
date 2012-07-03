//-
//Maya stand-alone applicatin plug-in

//How to use:
//Set MAYA_LOCATION env
//Set PYTHONPATH to %MAYA_LCATION%/bin/python26.zip
//Add %MAYA_LOCATION%/bin to PATH env

//How to build:
//Open %MAYA_LOCATION%/devkit/applications/asciiToBinary.sln
//Modify Project Properties-->Configuration Properties-->Linker-->System-->SubSystem-->windows
//+

#include <maya/MStatus.h>
#include <maya/MString.h> 
#include <maya/MFileIO.h>
#include <maya/MLibrary.h>
#include <maya/MIOStream.h>
#include <maya/MGlobal.h>
#include <string.h>

// Macro for error checking
#define checkErr(stat,msg)                  \
    if ( MS::kSuccess != stat ) {           \
        cerr << msg;                  		\
        return stat;                        \
    }

const char* usage = "usage: [-h/help] ma_mb fileName1 fileName2 ...\n\
       each file will be loaded, the filename will be checked for an\n\
       extension.  If .ma is found it will be change to .mb, otherwise a\n\
       .mb will be to the .ma.";

// replace all string
std::string&   replace_all_distinct(std::string&   str,const   std::string&   old_value,const   std::string&   new_value)   
{   
	for(std::string::size_type   pos(0);   pos!=std::string::npos;   pos+=new_value.length())   {   
		if(   (pos=str.find(old_value,pos))!=std::string::npos   )   
            str.replace(pos,old_value.length(),new_value);   
        else   break;   
    }   
    return   str;  
}   

//Use WinMain to support drag and drop multi-files to exe's icon
int WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	MStatus stat;
	MString newFile;
	MString fileExt;
	MString	fileName;

	// get file names
	std::string strfiles(lpCmdLine);
	// replace "\" with "/"
	strfiles = replace_all_distinct(strfiles,"\\","/");

	stat = MLibrary::initialize("Maya",true);

	if (!stat) {
		stat.perror("MLibrary::initialize");
		return 1;
	}

	MStringArray fileArray;
	MString temp(strfiles.c_str());
	temp.split(' ', fileArray);

    for (unsigned i = 0; i < fileArray.length(); i++)
    {
		fileName = fileArray[i];

		MString fileType;

		MFileIO::newFile(true);

		// Load the file into Maya
		stat = MFileIO::open(fileName);
		//if ( !stat ) {
		//	stat.perror(fileName.asChar());
		//	continue;
		//}

		// Delete unknown node
		MString cmd;
		cmd="{";
		cmd+="string $node,$nodes[]=`ls -type unknown -type unknownDag -type unknownTransform`;";
		cmd+="for($node in $nodes){";
		cmd+="lockNode -lock off $node;";
		cmd+="if(catch(`delete $node`)){";
        cmd+="	print (\"delete unknown node error: \" + $node);";
		cmd+="}";
		cmd+="else{";
        cmd+="	print (\"delete unknown node success: \" + $node);";
		cmd+="}";
		cmd+="}";
		cmd+="}";

		MGlobal::executeCommand(cmd);
//		// create an iterator to go through all nodes
//		MItDependencyNodes it(MFn::kUnknown);
//		//MItDag it(MItDag::kDepthFirst,MFn::kUnknownDag);
//		MDGModifier dgModifier;

//		unsigned i=0;
//		// keep looping until done
//		for(;!it.isDone();it.next())
//		{
//			cout << i << endl;
//			// get a handle to this node
//			MObject obj = it.item();
//
//
//			stat = dgModifier.deleteNode( obj );
//			checkErr( stat, "Could not delete node" );
//
//			dgModifier.doIt();
//
//			// write the node type found
//			//cout << obj.apiTypeStr() << endl;
//
//			// move on to next node
//
//			i ++;
//		}

		// Check for a file extension, change it to .mb.  
		

		int loc = fileName.rindex('.');
		newFile = fileName.substring(0, loc-1);
		int len = fileName.length();
		fileExt = fileName.substring(len-3, len-1);
		
		if( fileExt == ".ma" ){
			newFile += ".mb" ;
			stat = MFileIO::saveAs(newFile, "mayaBinary");
		}
		else{
			newFile += ".ma" ;
			stat = MFileIO::saveAs(newFile, "mayaAscii");
		}
		
		if (stat){
			cerr << fileExt << endl ;
			cerr << fileName
				 << ": resaved as "
			     << MFileIO::currentFile()
				 << endl;
		}
		else{
			stat.perror(newFile.asChar());
		}
	}

	MLibrary::cleanup();
	return 0;
}