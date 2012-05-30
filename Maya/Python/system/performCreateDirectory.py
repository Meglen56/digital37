import os
import traceback
import itertools

class PerformCreateDirectory():
    def __init__(self):
        self.Dir_Root = ''
        self.Dir_Framework = list()
        self.Dir_Name = dict()
        self.Dir_Acture = list()
        
    #self.Dir_Framework: [{['a']: ['1', '']}, {['b']: [{'2': ['I', 'II']}]}, ['c']]                                                                                 
    def create_directory(self,dir_root,dir_list):
        # create ep directory
        for f in dir_list:
            if type(f) is type('') :
                if f:
                    f = f.split() 
                    # for 'some name'
                    # create folder
                    for x in f :
                        self.make_dir(dir_root,x)
                else:
                    # skip for ''
                    pass
            elif type(f) is type(dict()) :
                #
                for k,v in f.iteritems() :
                    for x in k.split() :
                        root_dir = os.path.join(dir_root,x)
                        print 'root_dir:\t%s' % root_dir
                        self.create_directory(root_dir,v)
            else:
                print 'type error in dir_list'

    # make folders and files
    def make_dir(self,root,name):
        # replace '\' with '/'
        root = root.replace('\\','/')
        d = os.path.join(root,name)
        if not os.path.exists(d):
            if os.path.dirname(d) == d :
                # create folder
                if not os.path.exists(d):
                    try:
                        os.makedirs(d)
                    except:
                        traceback.print_exc()
            else :
                # create file
                # create folder first
                if not os.path.exists(os.path.dirname(d)):
                    try:
                        os.makedirs(os.path.dirname(d))
                    except:
                        traceback.print_exc()
                    else:
                        # create file
                        if not os.path.exists(d):
                            try:
                                fd = open(d,'w')
                            except:
                                traceback.print_exc()
                            else:
                                fd.close()
            
    def get_acture_name(self,sourceList):
        targetList = sourceList
        # self.Dir_Framework 
        # self.Dir_Name
        # self.Dir_Framework: [{'a': ['1', '']}, {'b': [{'2': ['I', 'II']}]}, 'c']   
        for l,i in zip(sourceList,xrange(len(sourceList))):
            # l = {'a': ['1', '']}
            # find 'a' and replace with acture name
            if type(l) is type(dict()) :
                # replace 'a' with acture name
                # replace ['1', ''] with acture name
                print 'l:\t%s' % l
                for k,v in l.iteritems():
                    returnList = self.get_acture_name(v)
                    # k = 'a' with no '+'
                    a = self.get_acture_name_2( k )
                    targetList[i] = {a:returnList}
            else :         
                # l = 'c' or l = 'c+d'
                targetList[i] = self.get_acture_name_2(l)
            print 'targetList\t%s' % targetList
        return targetList

    def get_acture_name_2(self,l):
        t = list()
        if l.find('+') == -1 :
            # l = 'c'
            if l in self.Dir_Name:# l in self.Dir_Name
                for x in self.Dir_Name[l].split() :
                    print 'x:\t%s' % x
                    t.append(x)
            else:# l not in self.Dir_Name
                # use l for value 
                t.append(l)
        else:
            # l = 'c+d'
            # split '+'
            t1 = list()
            for x in l.split('+') :
                tmp = list()
                if x in self.Dir_Name:# x in self.Dir_Name
                    for y in self.Dir_Name[x].split() :
                        tmp.append(y)
                    t1.append(tmp)
                else:# x not in self.Dir_Name
                    tmp.append(x)
                    t1.append(tmp)
            print 't1:\t%s' % t1
            
            # t1 = {'a': ['aa', 'bb'], 'b': ['bb', 'cc']}
            t1_product = list( self.product(t1) )
            print t1_product
            # t = [('aa', 'bb'), ('aa', 'cc'), ('bb', 'bb'), ('bb', 'cc')]
            for x in t1_product:
                t.append( ''.join(x) )
        t = ' '.join(t)
        print 't:\t%s' % t
        return t
                
    # from itertools's product function
    def product(self,inputList):
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        #pools = map(tuple, args) * kwds.get('repeat', 1)
        #pools = map(tuple, args) * kwds.get('repeat', 1)
        pools = list(x for x in inputList)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield list(prod)
            
    def perform_create_directory(self):
        print 'self.Dir_Root\t%s' % self.Dir_Root
        print 'self.Dir_Framework\t%s' % self.Dir_Framework
        print 'self.Dir_Name\t%s' % self.Dir_Name

        self.Dir_Acture = self.get_acture_name( self.Dir_Framework )
        print 'self.Dir_Acture\t%s' % self.Dir_Acture
        self.create_directory(self.Dir_Root, self.Dir_Acture)
                                    
def main():
    a = PerformCreateDirectory()
    a.Dir_Root='D:/Autodesk'
    a.Dir_Framework=[{'ep':[{'ep+x+shot': [{'type':['ep+x+shot+x+type+f']}]}]}]
    a.Dir_Name={'ep': 'ep010', 'shot': 'shot0010 shot0020', 'type': 'anim light vfx cam comp', 'x':'_', 'f':'.mb'}
    a.perform_create_directory()
    
if __name__ == '__main__' :
    #main()
    pass
    