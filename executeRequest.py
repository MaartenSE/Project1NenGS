'''
executeRequest creates a dictionary with all the
properties needed for creating a http response,
given a dictionary with all the properties of a http request
'''

import os.path

contentfolder   = 'content'
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
        filepath    = contentfolder + request['filepath']
        tagpath     = etagfolder + request['filepath'] + '.etag'
        
        if os.path.exists(filepath):
            #the requested file does exist
            #load the etag file
            ETag        = open(tagpath,"r").read()
            print('If-None-Match' in request['headers'])
            if 'If-None-Match' in request['headers'] and \
            request['headers']['If-None-Match'] == ETag:
                #the cached file is the most recent file
                print("file in cache")
                response['statuscode']      = "304"
                response['reasonphrase']    = "Not Modified"
            else:                
                #the cached file has been modified
                print("file does exist")
                file = open(filepath,"rb")
                
                response['statuscode']      = "200"
                response['reasonphrase']    = "OK"
                response['messagebody']     = file.read()
            #set the ETag    
            response['headers']['ETag'] = ETag
            
        else:
            #the requested file does not exist
            print("file does not exist")

            response['statuscode']      = "404"
            response['reasonphrase']    = "Not Found"


    
#fill the headers dictionary
    #Set the persistence of the connection
    response['headers']['Connection'] = 'close'
    
    # if there is a messagebody then set the response header for the content-length
    if 'messagebody' in response:
        response['headers']['Content-Length']=  str(len(response['messagebody']))

    return response

