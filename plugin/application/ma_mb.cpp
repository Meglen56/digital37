//-
//Maya stand-alone applicatin plug-in

//How to use:
//Set MAYA_LOCATION env
//Set PYTHONPATH to %MAYA_LCATION%/bin/python26.zip
//Add %MAYA_LOCATION%/bin to PATH env

//How to build:
//Open %MAYA_LOCATION%/devkit/applications/asciiToBinary.sln
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
       .mb will be to the .ma.\n\
	   should set env below:\n\
	   MAYA_LOCATION env\n\
	   PYTHONPATH to %MAYA_LCATION%/bin/python26.zip\n\
	   Add %MAYA_LOCATION%/bin to PATH env";

// replace all string
std::string&   replace_all_distinct(std::string&   str,
									const   std::string&   old_value,const   std::string&   new_value)   
{   
	for(std::string::size_type   pos(0);   pos!=std::string::npos;   pos+=new_value.length())   {   
		if(   (pos=str.find(old_value,pos))!=std::string::npos   )   
            str.replace(pos,old_value.length(),new_value);   
        else   break;   
    }   
    return   str;  
}   

// Delete unknown node command
void delete_nuknown_node()
{
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
}

int main(int argc, char **argv)
{
	MStatus stat;
	MString newFile;
	MString fileExt;
	MString	fileName;
	MString fileType;

	argc--, argv++;

	if (argc == 0) {
		cerr << usage;
		return(1);
	}

	for (; argc && argv[0][0] == '-'; argc--, argv++) {
		if (!strcmp(argv[0], "-h") || !strcmp(argv[0], "-help")) {
			cerr << usage;
			return(1);
		}
		// Check for other valid flags

		if (argv[0][0] == '-') {
			// Unknown flag
			cerr << usage;
			return(1);
		}
	}

	stat = MLibrary::initialize (argv[0]);
	if (!stat) {
		stat.perror("MLibrary::initialize");
		return 1;
	}
	
	for (int i = 0;i<argc;i++) {
		std::string strfiles(argv[i]);
		// replace "\" with "/"
		strfiles = replace_all_distinct(strfiles,"\\","/");
		// get file names
		fileName = strfiles.c_str();

		MFileIO::newFile(true);

		// Load the file into Maya
		stat = MFileIO::open(fileName);
		if ( !stat ) {
			stat.perror(fileName.asChar());
			continue;
		}
		
		// delete unknown node
		delete_nuknown_node();

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
			//cerr << fileExt << endl ;
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