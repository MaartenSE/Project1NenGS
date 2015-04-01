'''
executeRequest creates a dictionary with all the
properties needed for creating a http response,
given a dictionary with all the properties of a http request
'''

import os.path

#content is the folder containing the webpages of the server
contentfolder   = 'content'
#ETags is the folder containing the etags of all the webpages of the server
etagfolder      = 'ETags'

def executeRequest(request):
    #create a new dictionary for the reponse
    response = {}

    #Not the correct way of handling httpversions different than 1.1
    response['httpversion'] = request ['httpversion']

    #create an empty dictionary for the headers
    response['headers'] = {}

    #execute a GET request
    if request['method'] == "GET":
        #removing the first character
        requestpath    = contentfolder + request['requestpath']
        tagpath     = etagfolder + request['requestpath'] + '.etag'
        print("Requestpath ", requestpath)

        #Check if content does exist
        if os.path.isfile(requestpath):
            #the requested file does exist
            #load the etag file
            ETag        = open(tagpath,"r").read()
            
            if 'If-None-Match' in request['headers'] and \
            request['headers']['If-None-Match'] == ETag:
                #the cached file is the most recent file
                print("file in cache")
                response['statuscode']      = "304"
                response['reasonphrase']    = "Not Modified"
            else:                
                #the cached file has been modified
                print("file does exist")
                file = open(requestpath,"rb")
                
                response['statuscode']      = "200"
                response['reasonphrase']    = "OK"
                response['messagebody']     = file.read()
            #set the ETag    
            response['headers']['ETag'] = ETag

        #If the content does not exist check if a folder exist with requestpath
        #as its name containing a file index.html
        elif os.path.isfile(os.path.join(requestpath,'index.html')):
            print ("Folder requested returned folder/index.html")
            file = open(os.path.join(requestpath,'index.html'),"rb")
            
            response['statuscode']      = "301"
            response['reasonphrase']    = "Moved Permanently"
            response['messagebody']     = file.read()
        else:
            #the requested file does not exist
            print("file does not exist")

            response['statuscode']      = "404"
            response['reasonphrase']    = "Not Found"

        #To make it look good in the Shell =]
        print("")


    
#fill the headers dictionary
    #Set the persistence of the connection
    if 'Connection' in request['headers'] and \
    request['headers']['Connection']=='keep-alive':
        response['headers']['Connection'] = 'keep-alive'
    else:       
        response['headers']['Connection'] = 'close'
    
    # if there is a messagebody then set the response header for the content-length
    if 'messagebody' in response:
        response['headers']['Content-Length']=  str(len(response['messagebody']))

    return response

