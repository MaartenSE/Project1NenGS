from createResponse     import *
from executeRequest     import *
from parseRequest       import *
import TCPSelectServer2

def HTTPserver(data):
#    request = parseRequest(data)
#    result = executeRequest(request)
#    response = createResponse(result)
#    return response
    print (data)

TCPSelectServer2.runServer(HTTPserver)

    
