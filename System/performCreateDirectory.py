import os
import traceback

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
                    for x in k :
                        root_dir = os.path.join(dir_root,x)
                        self.create_directory(root_dir,v)
            else:
                print 'type error in dir_list'

    def make_dir(self,root,name):
        d = os.path.join(root,name)
        if not os.path.exists(d):
            try:
                os.makedirs(d)
            except:
                traceback.print_exc()
                
#    def get_acture_name(self,sourceList):
#        targetList = sourceList
#        # self.Dir_Framework 
#        # self.Dir_Name
#        # self.Dir_Framework: [{'a': ['1', '']}, {'b': [{'2': ['I', 'II']}]}, 'c']   
#        for l,i in zip(sourceList,xrange(len(sourceList))):
#            # l = {'a': ['1', '']}
#            # find 'a' and replace with acture name
#            if type(l) is type(dict()) :
#                # replace 'a' with acture name
#                # replace ['1', ''] with acture name
#                print 'l:\t%s' % l
#                for k,v in l.iteritems():
#                    k = self.Dir_Name[k]
#                    returnList = self.get_acture_name(v)
#                    targetList[i] = {k:returnList}
#            else :
#                # l = 'c'
#                targetList[i] = self.Dir_Name[l]
#            print 'targetList\t%s' % targetList
#        return targetList
        
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
            for x in self.Dir_Name[l].split() :
                print 'x:\t%s' % x
                t.append(x)
        else:
            # l = 'c+d'
            # split '+'
            t1 = dict()
            for x in l.split('+') :
                t1[x] = list()
                for y in self.Dir_Name[x].split() :
                    t1[x].append(y)
            print 't1:\t%s' % t1
            
            li = list()
            # t1 = {'a': ['aa', 'bb'], 'b': ['bb', 'cc']}
            for v in t1.itervalues() :
                # v = ['aa', 'bb']
                if type(v) is not type('') :
                    # x = 'aa' 
                    for x in v :
                        li.append( v + x )
                else:
                    li.append( v )
            print 'li:\t%s' % li
                                            
            t.append(li)
        print 't:\t%s' % t
        
        s = ''
        for x in t:
            for y in x:
               s = ' '.join(y) 
        return s
                    
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
    a.Dir_Framework=[{'a': ['1']}, 'b+a']
    a.Dir_Name={'a': 'aa bb', '1': '111', 'b': 'bb cc'}
    a.perform_create_directory()
    
if __name__ == '__main__' :
    main()
    