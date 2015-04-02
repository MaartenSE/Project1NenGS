'''
create Etags of all the content on the server
'''

import os.path
import hashlib
import shutil
import time

contentfolder   = 'Content'
etagfolder      = 'ETags'

#create a hash object
hashobject  = hashlib.sha256()

def buildEtags():

    #remove the old Etags
    if os.path.isdir(etagfolder):
        shutil.rmtree(etagfolder)

    #wait for operating system to remove the old folder
    time.sleep(0.001)
    #create a new folder Etags and fill the folder
    os.mkdir(etagfolder)
    _recursiveHash("")
    
def _recursiveHash(path):
    for name in os.listdir(os.path.join(contentfolder, path)):
        if os.path.isdir(os.path.join(contentfolder, path, name)):
            os.mkdir(os.path.join(etagfolder, path, name ))
            _recursiveHash(os.path.join(path, name))
        else:
            #open the original file
            #original = open(contentfolder + path + name,'r')
            #Make an Etag file for the file
            file = open(os.path.join(etagfolder, path, name + '.etag'), 'w')
            print(os.path.join(contentfolder, path, name))
            hashobject.update(open(os.path.join(contentfolder, path, name) ,'r').read())
            file.write(hashobject.digest())

