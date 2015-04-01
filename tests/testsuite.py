import unittest
import time
from socket import *
import sys

#Carriage return line feed
CRLF = '\r\n'

class TestStringMethods(unittest.TestCase):
#GET for an existing single resource
  def test_getExistingResource(self):
      serverName = 'localhost'
      serverPort = 8080
      clientSocket = socket(AF_INET, SOCK_STREAM)
      clientSocket.connect((serverName, serverPort))
      request = 'GET /existingresource.html HTTP/1.1' + CRLF + 'Host: localhost:8080'+ CRLF + 'Connection: keep-alive' + CRLF + 'Cache-Control: max-age=0' + CRLF + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' + CRLF + 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' + CRLF + 'Accept-Encoding: gzip, deflate, sdch' + CRLF + 'Accept-Language: de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4' + CRLF + CRLF
      clientSocket.send(request)
      receivedData = clientSocket.recv(4096)
      clientSocket.close()
      
      requestline, remainingrequest = receivedData.split(CRLF, 1)
      http, number, okindicator = requestline.split(' ', 2)
      #print okindicator
      self.assertEqual(okindicator, 'OK')
	  
#GET for a single resource that doesn't exist
  def test_getNonExistingResource(self):
      serverName = 'localhost'
      serverPort = 8080
      clientSocket = socket(AF_INET, SOCK_STREAM)
      clientSocket.connect((serverName, serverPort))
      request = 'GET /nononothing.html HTTP/1.1' + CRLF + 'Host: localhost:8080'+ CRLF + 'Connection: keep-alive' + CRLF + 'Cache-Control: max-age=0' + CRLF + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' + CRLF + 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' + CRLF + 'Accept-Encoding: gzip, deflate, sdch' + CRLF + 'Accept-Language: de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4' + CRLF + CRLF
      clientSocket.send(request)
      receivedData = clientSocket.recv(4096)
      clientSocket.close()
      
      requestline, remainingrequest = receivedData.split(CRLF, 1)
      http, errorcode, okindicator = requestline.split(' ', 2)
      #print errorcode
      self.assertEqual(errorcode, '404')
	  
#GET for an existing single resource followed by a GET for that same resource, with caching utilized on the client/tester side
  def test_getCachingResource(self):
      serverName = 'localhost'
      serverPort = 8080
      clientSocket = socket(AF_INET, SOCK_STREAM)
	  
      clientSocket.connect((serverName, serverPort))
      request1 = 'GET /cachable.html HTTP/1.1' + CRLF + 'Host: localhost:8080'+ CRLF + 'Connection: keep-alive' + CRLF + 'Cache-Control: max-age=0' + CRLF + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' + CRLF + 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' + CRLF + 'Accept-Encoding: gzip, deflate, sdch' + CRLF + 'Accept-Language: de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4' + CRLF + CRLF
      clientSocket.send(request1)
      receivedData1 = clientSocket.recv(4096)  
	  #get etag from received data
      request1, connection1, etag1 = receivedData1.split(CRLF,2)
      etagHeader, etagValue = etag1.split(' ', 1)
      #print 'receivedETAG1: ' + etagValue
     
      
      request2 = 'GET /cachable.html HTTP/1.1' + CRLF + 'Host: localhost:8080'+ CRLF + 'Connection: keep-alive' + CRLF + 'Cache-Control: max-age=0' + CRLF + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' + CRLF + 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' + CRLF + 'Accept-Encoding: gzip, deflate, sdch' + CRLF + 'Accept-Language: de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4' + CRLF + 'If-None-Match: ' + etagValue + CRLF + CRLF
      clientSocket.send(request2)
      receivedData2 = clientSocket.recv(4096)
      clientSocket.close()
      
      requestline, remainingrequest = receivedData2.split(CRLF, 1)
      http, statuscode, okindicator = requestline.split(' ', 2)
      #print 'receivedData1 \n' + receivedData1
      #print 'receivedData2 \n' + receivedData2
      self.assertEqual(statuscode, '304')
      
#GET for a directory with an non-existing index.html file
  def test_getDirectoryWithoutIndex(self):
      serverName = 'localhost'
      serverPort = 8080
      clientSocket = socket(AF_INET, SOCK_STREAM)
      clientSocket.connect((serverName, serverPort))
      request = 'GET /somedirectory/ HTTP/1.1' + CRLF + 'Host: localhost:8080'+ CRLF + 'Connection: keep-alive' + CRLF + 'Cache-Control: max-age=0' + CRLF + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' + CRLF + 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' + CRLF + 'Accept-Encoding: gzip, deflate, sdch' + CRLF + 'Accept-Language: de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4' + CRLF + CRLF
      clientSocket.send(request)
      receivedData = clientSocket.recv(4096)
      clientSocket.close()
      receivedData
      requestline, remainingrequest = receivedData.split(CRLF, 1)
      http, errorcode, okindicator = requestline.split(' ', 2)
      #print errorcode
      self.assertEqual(errorcode, '404')
	  
#GET for a directory with existing index.html file
  def test_getDirectoryWitIndex(self):
      serverName = 'localhost'
      serverPort = 8080
      clientSocket = socket(AF_INET, SOCK_STREAM)
      clientSocket.connect((serverName, serverPort))
      request = 'GET /somedirectoryIndex/ HTTP/1.1' + CRLF + 'Host: localhost:8080'+ CRLF + 'Connection: keep-alive' + CRLF + 'Cache-Control: max-age=0' + CRLF + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' + CRLF + 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' + CRLF + 'Accept-Encoding: gzip, deflate, sdch' + CRLF + 'Accept-Language: de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4' + CRLF + CRLF
      clientSocket.send(request)
      receivedData = clientSocket.recv(4096)
      clientSocket.close()
      receivedData
      requestline, remainingrequest = receivedData.split(CRLF, 1)
      http, errorcode, okindicator = requestline.split(' ', 2)
      #print errorcode
      self.assertEqual(errorcode, '301')
	  
#multiple GETs over the same (persistent) connection with the last GET prompting closing the connection, the connection should be closed

#multiple GETs over the same (persistent) connection, followed by a wait during which the connection times out, the connection should be closed

#multiple GETs, some of which are parallel (think of the situation when your browser is fetching a composite resource), the responses should be sent in an orderly fashion

if __name__ == '__main__':
    unittest.main()
