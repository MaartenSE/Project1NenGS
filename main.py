'''
The main file for project 1 for Netwerken en gedistribueerde systemen.
'''
from buildEtags         import *
from parseRequest       import *
from executeRequest     import *
from createResponse     import *
from TCPSelectServer2   import *

'''
The HTTPserver function implements (some) of the behavior specified in
http://tools.ietf.org/html/rfc2616
It divides the function
'''
def HTTPserver(HTTPrequest):
    
    #parse the request
    request = parseRequest(HTTPrequest)

    #create a response
    response = executeRequest(request)

    #construct and return the response
    return createResponse(response)

#update the ETags
buildEtags()
#And run the server!
runServer(HTTPserver)

    
