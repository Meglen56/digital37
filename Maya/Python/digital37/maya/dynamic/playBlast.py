import digital37.maya.animation.playBlast.PlayBlast as PlayBlast  
        
def main(width=None,height=None,quicktime_settings_file=None):
    a = PlayBlast()
    a.get_file_logger()
    a.set_quicktime_settings(quicktime_settings_file)
    a.set_pb_name_by_folder('playblast_sim')
    # TODO 128 will be return in some pc when do playblast
    a.set_subprocess_returnCode([0,128])
    a.playBlast(width,height)
    
if __name__ == '__main__' :
    pass
    #main()
