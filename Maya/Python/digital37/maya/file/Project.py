import os
import tempfile

class Project():
    def __init__(self,root_directory):
        self.get_root(root_directory)
        
        
    def init_shot(self,eposides,shots):
        self.get_eposide(eposides)
        self.get_shot(shots)
        self.get_shot_types()
        
    def get_root(self,root_directory):
        self.Root_Directory = root_directory
        
    def get_eposide(self,eposides):
        self.Eposides = eposides.split()
        
    def get_shot(self,shots):
        self.Shots = shots.split()
        
    def get_shot_types(self):
        #self.Shot_Types = {'anim':'an','layout':'ly','vfx':'vfx','comp':'comp','cam':'cam','light':'light'}
        #self.Shot_Types = {'light':'light'}
        self.Shot_Types = {'render':'render'}
            
    def create_directory_shot2(self):
        # create ep directory
        for eposide in self.Eposides:
            for shot in self.Shots:
                for shot_type,shot_type_name in self.Shot_Types.iteritems():
                    d = os.path.join(self.Root_Directory,'scenes/shot',eposide,(eposide+'_'+shot),shot_type)
                    print d
                    if not os.path.exists(d):
                        os.makedirs(d)
                    f = 'seer_'+shot_type_name+'_'+eposide+'_'+shot+'.mb'
                    fileName = os.path.join(d,f)
                    if not os.path.exists(fileName):
                        fd = open(fileName,'w')
                        fd.close()
                                        
    def create_directory_shot(self):
        # create ep directory
        for eposide in self.Eposides:
            for shot in self.Shots:
                for shot_type,shot_type_name in self.Shot_Types.iteritems():
                    d = os.path.join(self.Root_Directory,'scenes/shot',eposide,(eposide+'_'+shot),shot_type)
                    print d
                    if not os.path.exists(d):
                        os.makedirs(d)
                        f = 'seer_'+shot_type_name+'_'+eposide+'_'+shot+'.mb'
                        if shot_type == 'comp' :
                            f = 'seer_'+shot_type_name+'_'+eposide+'_'+shot+'.nk'
                        fileName = os.path.join(d,f)
                        if not os.path.exists(fileName):
                            fd = open(fileName,'w')
                            fd.close()
            
    def create_directory_asset(self,asset_type,assets):
        # create ep directory
        for asset in assets.split():
            for asset_folder in ['high','shading','rig','blendShape','low']:
                d = os.path.join(self.Root_Directory,'scenes','asset',asset_type,asset,asset_folder)
                if not os.path.exists(d):
                    os.makedirs(d)
                    f = asset+'_'+asset_folder+'.mb'
                    fileName = os.path.join(d,f)
                    if not os.path.exists(fileName):
                        fd = open(fileName,'w')
                        fd.close()
            
    def create_directory_sourceimages(self,asset_type,assets):
        # create ep directory
        for asset in assets.split():
                d = os.path.join(self.Root_Directory,'sourceimages',asset_type,asset)
                if not os.path.exists(d):
                    os.makedirs(d)
                                                                
    def create_directory3(self,dirs,l1,l2):
        # create ep directory
        for shot in l2.split():
            for dir in dirs.split():
                d = os.path.join(self.Root_Directory,l1,(l1+'_'+shot),dir)
                if not os.path.exists(d):
                    os.makedirs(d)
                                                                                        
    def create_directory2(self):
        # create ep directory
        for eposide in self.Eposides:
            for shot in self.Shots:
                for shot_type,shot_type_name in self.Shot_Types.iteritems():
                    #d = os.path.join(self.Root_Directory,'scenes/shot',eposide,(eposide+'_'+shot),shot_type)
                    d = os.path.join(self.Root_Directory,eposide,(eposide+'_'+shot))
                    if not os.path.exists(d):
                        os.makedirs(d)
#                        f = 'seer_'+shot_type_name+'_'+eposide+'_'+shot+'.mb'
#                        if shot_type == 'comp' :
#                            f = 'seer_'+shot_type_name+'_'+eposide+'_'+shot+'.nk'
#                        fileName = os.path.join(d,f)
#                        if not os.path.exists(fileName):
#                            fd = open(fileName,'w')
#                            fd.close()
                                    
def main():
    #a = Project('d:/seer','ep01','sc0010 sc0011 sc0012 sc0013 sc0020 sc0021 sc0030 sc0031 sc0040 sc0041 sc0050 sc0060 sc0070 sc0080 sc0081 sc0090 sc0100 sc0110 sc0120 sc0130 sc0131 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0340 sc0350 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0440 sc0450 sc0460 sc0480 sc0490 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0660 sc0661 sc0662 sc0663 sc0670 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0731 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0820 sc0830 sc0840 sc0850 sc0870 sc0880 sc0890 sc0891 sc0892 sc0893 sc0894 sc0895 sc0910 sc0920 sc0930 sc0940 sc0950 sc0951')
    #a = Project('d:/seer','ep02','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0210 sc0230 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0302 sc0310 sc0330 sc0340 sc0350 sc0360 sc0380 sc0400 sc0420 sc0430 sc0450 sc0460 sc0470 sc0480 sc0490 sc0530 sc0540')
    #a = Project('d:/seer','ep03a','sc0010 sc0011 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0071 sc0072 sc0073 sc0080 sc0090 sc0100 sc0110')
    #a = Project('d:/seer','ep03b','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0510')
    #a = Project('d:/seer','ep04','sc0010 sc0020 sc0040 sc0041 sc0050 sc0060 sc0061 sc0070 sc0080 sc0090 sc0110 sc0111 sc0130 sc0140 sc0150')
    #a = Project('d:/seer','ep05','sc0010 sc0030 sc0040 sc0050 sc0060 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0150 sc0160 sc0170 sc0190 sc0220 sc0230 sc0240 sc0270 sc0290 sc0300 sc0310 sc0320 sc0330')
    #a = Project('d:/seer','ep06','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0080 sc0090 sc0100 sc0120 sc0130 sc0140 sc0150 sc0151 sc0160 sc0170')
    #a = Project('d:/seer','ep07','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0410 sc0420 sc0430 sc0440 sc0450 sc0470 sc0480 sc0500 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600')
    #a = Project('d:/seer','ep08','sc0020 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0130 sc0140 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0651 sc0670 sc0690 sc0700 sc0710 sc0720 sc0740 sc0750 sc0751 sc0760 sc0770 sc0780 sc0800 sc0801 sc0802 sc0820 sc0830 sc0840 sc0850 sc0870 sc0880 sc0890 sc0900 sc0920 sc0930 sc0940 sc0950 sc0970 sc0980 sc0990 sc1000 sc1010 sc1020 sc1040 sc1050 sc1060 sc1070 sc1080 sc1090 sc1100 sc1110 sc1120 sc1130 sc1140 sc1150 sc1160 sc1170 sc1180 sc1190 sc1200 sc1210 sc1220 sc1230 sc1240 sc1250 sc1260 sc1270 sc1280 sc1290 sc1300 sc1310 sc1320 sc1330 sc1340 sc1350 sc1360 sc1370 sc1380 sc1390 sc1440 sc1450 sc1460 sc1470 sc1480 sc1490 sc1491 sc1492 sc1500 sc1510 sc1520 sc1530 sc1540 sc1560 sc1580 sc1590 sc1600 sc1610 sc1620 sc1630 sc1640 sc1650 sc1670 sc1680 sc1690 sc1700 sc1710 sc1720 sc1721 sc1722 sc1730 sc1740 sc1750 sc1760 sc1770 sc1780 sc1790 sc1800 sc1810 sc1820 sc1821 sc1830 sc1840')
    #a = Project('d:/seer','ep09','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350')
    #a = Project('d:/seer','ep10','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0660 sc0670 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0800 sc0810 sc0820 sc0830 sc0840 sc0850 sc0860 sc0870 sc0880 sc0890 sc0900 sc0910 sc0920 sc0930 sc0940 sc0950 sc0960 sc0970 sc0980 sc0990 sc1000 sc1010 sc1020 sc1030 sc1040 sc1050 sc1060 sc1070 sc1080 sc1090 sc1100 sc1110 sc1120 sc1130 sc1140 sc1150 sc1160 sc1170 sc1180 sc1190 sc1200 sc1210 sc1220 sc1230 sc1240 sc1250 sc1260 sc1270 sc1280 sc1290 sc1300 sc1310 sc1320 sc1330 sc1340 sc1350 sc1360 sc1370 sc1380 sc1390 sc1400 sc1410 sc1420 sc1430 sc1440 sc1450 sc1460 sc1470 sc1480 sc1490 sc1500 sc1510 sc1520 sc1530 sc1540 sc1550 sc1560 sc1570 sc1580 sc1590 sc1600 sc1610 sc1620 sc1630 sc1640 sc1650 sc1660 sc1670 sc1680 sc1690 sc1700 sc1710 sc1720 sc1730 sc1740 sc1750 sc1760 sc1770 sc1780 sc1790 sc1800 sc1810 sc1820 sc1830 sc1840 sc1850 sc1860')
    #a = Project('d:/seer','ep11','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0130 sc0140 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0490 sc0500 sc0510')
    #a = Project('d:/seer','ep12','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0090 sc0100 sc0101 sc0130 sc0140 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320')
    #a = Project('d:/seer','ep13','sc0010 sc0020 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0291')
    #a = Project('d:/seer','ep14','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0081 sc0090 sc0100 sc0101 sc0110 sc0120 sc0130 sc0140 sc0141 sc0150 sc0160 sc0161 sc0170 sc0180 sc0190 sc0191 sc0200 sc0210 sc0211 sc0220 sc0230 sc0231 sc0240 sc0250 sc0251 sc0260 sc0270 sc0271 sc0280 sc0281 sc0290 sc0300 sc0310 sc0340 sc0341 sc0350 sc0360')
    #a = Project('d:/seer','ep15','sc0010 sc0020 sc0030 sc0060 sc0061 sc0080 sc0090 sc0091 sc0120 sc0121 sc0130 sc0160 sc0170 sc0180 sc0181 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0251 sc0260 sc0280 sc0290 sc0300 sc0310 sc0311 sc0320 sc0330 sc0331 sc0332 sc0340 sc0350 sc0360 sc0370 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0441 sc0450 sc0460 sc0461 sc0480 sc0490 sc0510 sc0511 sc0520 sc0530 sc0540 sc0550 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0660 sc0670 sc0690 sc0710 sc0720 sc0721 sc0730 sc0740 sc0750')
    #a = Project('d:/seer','ep16','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320')
    #a = Project('d:/seer','ep17','sc0010 sc0020 sc0021 sc0030 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0441 sc0450 sc0470 sc0480 sc0490 sc0500 sc0510 sc0511 sc0520 sc0530 sc0540 sc0550 sc0551 sc0552 sc0553 sc0554 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0660 sc0670 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0800 sc0810 sc0820 sc0830')
    #a = Project('d:/seer','ep18','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0420 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0501 sc0510 sc0520 sc0530 sc0560 sc0570 sc0580 sc0590 sc0600 sc0620 sc0640 sc0650 sc0660 sc0670 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0800 sc0810 sc0820 sc0830 sc0840 sc0850 sc0870 sc0880 sc0890 sc0900 sc0910 sc0920 sc0961 sc0970 sc0980 sc0990 sc1000 sc1010 sc1020 sc1030')
    #a = Project('d:/seer','ep19','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0090 sc0100 sc0111 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210')
    #a = Project('d:/seer','ep20','sc0010 sc0011 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0110 sc0120')
    #a = Project('d:/seer','ep22','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120')
    #a = Project('d:/seer','ep23','sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0470 sc0480 sc0490 sc0500 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0611 sc0620 sc0630 sc0640 sc0650 sc0670 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0800 sc0810 sc0820 sc0830 sc0840 sc0850 sc0860')
    #a = Project('d:/seer','ep24','sc0010 sc0030 sc0040 sc0050 sc0060 sc0110')
    #a = Project('d:/seer','ep25','sc0010 sc0011 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0260 sc0270 sc0290 sc0300 sc0310 sc0320 sc0330')
    #a = Project('d:/seer','ep26','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400')
    #a = Project('d:/seer','ep27','sc0010')
    #a = Project('d:/seer','ep28','sc0010 sc0020 sc0030 sc0040 sc0041 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0231 sc0251 sc0260 sc0261 sc0270 sc0320')
    #a = Project('d:/seer','ep29','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0100 sc0101 sc0110 sc0120 sc0130 sc0140 sc0150 sc0151 sc0160 sc0170 sc0190 sc0200 sc0201 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0660 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0790 sc0820 sc0830 sc0840 sc0850 sc0860 sc0870 sc0880 sc0890 sc0900 sc0910')
    #a = Project('d:/seer','ep30','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0660 sc0670 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0800 sc0810 sc0820 sc0830 sc0840 sc0850 sc0860 sc0870 sc0880 sc0890 sc0900 sc0910 sc0920 sc0930 sc0940 sc0950 sc0960 sc0970 sc0980 sc0990 sc1000 sc1010 sc1020 sc1030 sc1040 sc1050 sc1060 sc1070 sc1080 sc1090 sc1100 sc1110 sc1120 sc1130 sc1140 sc1150 sc1160 sc1170 sc1180 sc1190 sc1200 sc1210 sc1220 sc1230 sc1240 sc1250 sc1260 sc1270 sc1280 sc1290 sc1300 sc1310 sc1320 sc1330 sc1340 sc1350 sc1360 sc1370 sc1380 sc1390 sc1400 sc1410 sc1420 sc1430 sc1440 sc1450 sc1460 sc1470 sc1480 sc1490 sc1500 sc1510 sc1520 sc1530 sc1540 sc1550 sc1560 sc1570 sc1580 sc1590 sc1600 sc1610 sc1620 sc1630 sc1640 sc1650 sc1660 sc1670 sc1680 sc1690 sc1700 sc1710 sc1720 sc1730 sc1740 sc1750 sc1760 sc1770 sc1780 sc1790 sc1800 sc1810 sc1820 sc1830 sc1840 sc1850 sc1860 sc1870 sc1880 sc1890 sc1900 sc1910 sc1920 sc1930 sc1940 sc1950 sc1960 sc1970 sc1980 sc1990 sc2000 sc2010 sc2020 sc2030 sc2040 sc2050 sc2060 sc2070 sc2080 sc2090 sc2100 sc2110 sc2120 sc2130 sc2140 sc2150 sc2160 sc2170 sc2180 sc2190 sc2200 sc2210 sc2220 sc2230 sc2240 sc2250 sc2260 sc2270 sc2280 sc2290 sc2300 sc2310 sc2320 sc2330 sc2340 sc2350 sc2360 sc2370 sc2380 sc2390 sc2400 sc2410 sc2420 sc2430 sc2440 sc2450 sc2460 sc2470 sc2480 sc2490 sc2500 sc2510 sc2520 sc2530 sc2540 sc2550 sc2560 sc2570 sc2580 sc2590 sc2600 sc2610 sc2620 sc2630 sc2640 sc2650 sc2660 sc2670 sc2680 sc2690 sc2700 sc2710')
    #a = Project('d:/seer','ep31','sc0010')
    #a = Project('d:/seer','ep32','sc0010 sc0020 sc0030 sc0031 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0510 sc0520 sc0530 sc0540 sc0541 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620')
    #a.create_directory()
    #a = Project('d:/rovio','ep01','sc0020 sc0040')
    #a.create_directory()
    
    # Create image sequence
    #a=Project('Z:/seerSequence','ep01','sc0010 sc0011 sc0012 sc0013 sc0020 sc0021 sc0030 sc0031 sc0040 sc0041 sc0050 sc0060 sc0070 sc0080 sc0081 sc0090 sc0100 sc0110 sc0120 sc0130 sc0131 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0340 sc0350 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0440 sc0450 sc0460 sc0480 sc0490 sc0510 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0650 sc0660 sc0661 sc0662 sc0663 sc0670 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0731 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0820 sc0830 sc0840 sc0850 sc0870 sc0880 sc0890 sc0891 sc0892 sc0893 sc0894 sc0895 sc0910 sc0920 sc0930 sc0940 sc0950 sc0951')
    #a=Project('Z:/seerSequence','ep29','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0100 sc0101 sc0110 sc0120 sc0130 sc0140 sc0150 sc0151 sc0160 sc0170 sc0190 sc0200 sc0201 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0640 sc0660 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0790 sc0820 sc0830 sc0840 sc0850 sc0860 sc0870 sc0880 sc0890 sc0900 sc0910')
    #a.create_directory2()
#    a=Project('d:/rovio')
#    a.create_directory_sourceimages('prop','egg cap')
#    a.create_directory_sourceimages('set','set01')
#    a.create_directory_sourceimages('character','blue_a blue_b blue_c red_s red_b black yellow')
#    a.create_directory_asset('character','blue_a blue_b blue_c red_s red_b black yellow')
#    a.create_directory_asset('set','set01')
#    a.create_directory_asset('prop','egg cap')

    #a = Project('Z:/D031SEER/sequence')
    #a.create_directory3('vfx render output','ep14','sc0010 sc0020')
    #a.create_directory3('vfx render output','ep29','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0100 sc0101 sc0110 sc0120 sc0130 sc0140 sc0150 sc0151 sc0160 sc0170 sc0190 sc0200 sc0201 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0420 sc0430 sc0440 sc0450 sc0460 sc0470 sc0480 sc0490 sc0500 sc0520 sc0530 sc0550 sc0560 sc0570 sc0580 sc0590 sc0600 sc0610 sc0620 sc0630 sc0631 sc0640 sc0660 sc0680 sc0690 sc0700 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0790 sc0820 sc0830 sc0840 sc0850 sc0860 sc0870 sc0880 sc0900 sc0910')
    a = Project('Z:/D031SEER/sequence')
    a.create_directory3('vfx render output','ep30b','sc0010a sc0010b sc0010c sc0010d sc0010e sc0010e1 sc0010e2 sc0010e3 sc0010f sc0010g sc0010g1 sc0010g2 sc0010h sc0100 sc0110 sc0120 sc0150 sc0180 sc0190 sc0200 sc0220 sc0230 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0351 sc0360 sc0370 sc0380 sc0390 sc0400 sc0410 sc0440 sc0450 sc0460 sc0470 sc0480 sc0520 sc0530 sc0540 sc0550 sc0560 sc0570 sc0580 sc0600 sc0620 sc0630 sc0650 sc0660 sc0670 sc0680 sc0690 sc0710 sc0720 sc0730 sc0740 sc0750 sc0760 sc0770 sc0780 sc0790 sc0791 sc0800 sc0801 sc0810a sc0810a1 sc0810a2 sc0810a3 sc0810b sc0810b1 sc0810c sc0810d sc0820 sc0820a sc0820b sc0821 sc0840 sc0850 sc0860 sc0870 sc0880 sc0890 sc0891 sc0900 sc0910 sc0920 sc0921 sc0930 sc0940 sc0950 sc0960 sc0970 sc0971 sc0972 sc0973 sc0974 sc0975 sc0975b sc0975c sc0976 sc0990 sc1010 sc1020 sc1040 sc1050 sc1060 sc1070 sc1080 sc1090 sc1100 sc1110 sc1120 sc1130 sc1140 sc1160 sc1161 sc1162 sc1163 sc1200 sc1201 sc1202 sc1210 sc1211 sc1220 sc1280 sc1290 sc1320 sc1330 sc1340 sc1370 sc1371 sc1380 sc1390 sc1391 sc1400')
    #a.init_shot('ep02','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0070 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0210 sc0230 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0302 sc0310 sc0330 sc0340 sc0350 sc0360 sc0380 sc0400 sc0420 sc0430 sc0450 sc0460 sc0470 sc0480 sc0490 sc0530 sc0540')
    #a.init_shot('ep26','sc0010 sc0020 sc0030 sc0040 sc0050 sc0060 sc0080 sc0090 sc0100 sc0110 sc0120 sc0130 sc0140 sc0150 sc0160 sc0170 sc0180 sc0190 sc0200 sc0210 sc0220 sc0230 sc0240 sc0250 sc0260 sc0270 sc0280 sc0290 sc0300 sc0310 sc0320 sc0330 sc0340 sc0350 sc0360 sc0370 sc0380 sc0390 sc0400')
    #a.create_directory_shot2()
        
if __name__ == '__main__' :
    main()
    