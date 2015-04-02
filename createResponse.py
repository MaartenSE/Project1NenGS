'''
function that creates the responsemessage
'''
#Carriage return line feed
CRLF = '\r\n'

def createResponse (response):
    
    #create the statusline
    statusline = \
               response['httpversion']  + ' ' +\
               response['statuscode']   + ' ' +\
               response['reasonphrase'] + CRLF

    #create the headers
    headers =''
    for k in response['headers']:
        headers += k + ': ' + response['headers'][k] + CRLF
    
    #combine all parts into the whole response message
    httpresponse = \
        statusline + \
        headers +\
        CRLF

    if 'messagebody' in response:
        httpresponse += response['messagebody']

    return httpresponse
