#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle https://github.com/tywtyw2002, and https://github.com/treedust
#
# Modified by Matthew Dekinder
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib, urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port=80):
        #adapted from https://github.com/joshua2ua/cmput404w17lab2 by Joshua Campbell
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port)) #clientSocket.connect(("www.google.com", 80))

        return clientSocket

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        parsedurl = urlparse.urlparse(url)
        #print parsedurl, '-------------________________-____________-----'
        host = parsedurl.netloc
        path = parsedurl.path
        #"http://%s:%d/%s" % (BASEHOST,BASEPORT, path)
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 80

        #print host, path, url, port

        req = 'GET '+ path +' HTTP/1.1\r\n'
        req += 'Host:' + host + '\r\n'
        req += 'Accept: */*\r\nUser-Agent: MattClient\r\nConnection: Close\r\n\r\n'

        socket = self.connect(host, port);

        socket.sendall(req)
        res = self.recvall(socket)
        #print res, '---------------------------------------'
        code = int(res.split(' ')[1])
        body = res.split('\r\n\r\n')[1]

        #print 'Code: ', code, ' Body: ', body

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        parsedurl = urlparse.urlparse(url)
        #print parsedurl, '-------------________________-____________-----'
        host = parsedurl.netloc
        path = parsedurl.path
        #"http://%s:%d/%s" % (BASEHOST,BASEPORT, path)
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 80

        urlArgs = '' #len('') = 0, so this works for no body
        if args is not None:
            urlArgs = urllib.urlencode(args)
        #print '****--------*****--',args, urllib.urlencode(args)

        req = 'POST '+ path +' HTTP/1.1\r\n'
        req += 'Host:' + host + '\r\n'
        req += 'Content-Length: '+str(len(urlArgs))+'\r\n'
        req += 'Accept: */*\r\nUser-Agent: MattClient\r\nConnection: Close\r\n\r\n'

        if args is not None:
            req+= urlArgs

        socket = self.connect(host, port);

        socket.sendall(req)
        res = self.recvall(socket)
        #print '____-_____------____---', res, '------______________-----------------------'
        code = int(res.split(' ')[1])
        body = res.split('\r\n\r\n')[1]
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
