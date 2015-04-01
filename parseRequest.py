'''
ParseRequest parses a HTTP request into a dictionary
'''
import re

#Carriage return line feed
CRLF = '\r\n'

def parseRequest (HTTPrequest):
    #create an empty dictionary
    request = {}
    requestline, remainingrequest = HTTPrequest.split(CRLF, 1)
    headers, messagebody = remainingrequest.split(CRLF+CRLF, 1)
    headers += CRLF
    request['messagebody'] = messagebody
    
    #put the headers into a new dictionary using a regular expression.
    #update the request dictionary with the new dictionary
    request['headers'] = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers))

    request['method'], request['requestpath'], request['httpversion'] = requestline.split(' ', 2)
 
    return request
