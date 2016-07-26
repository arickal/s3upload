from os import curdir
import os 
from os.path import join as pjoin
import tinys3
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import time

class StoreHandler(BaseHTTPRequestHandler):
    conn = []

    # def __init__(self):    
    #   conn = tinys3.Connection('AKIAIW5DLBV7L7CDGXAQ',
    #     'QHH7bIgA0BmEc4fUwdvGrNJvUuwWoD86N9zXZ4PH',tls=True)

    def do_GET(self):
        if self.path == '/store.json':
            with open(self.store_path) as fh:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(fh.read().encode())

    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
            filename = str(int(time.time()*1000)) + '_' + form['file'].filename
            data = form['file'].file.read()
            open("%s"%filename, "wb").write(data)

            f = open(filename,'rb')
            if self.conn==[]:
                print 'init conn'
                self.conn = tinys3.Connection('AKIAIW5DLBV7L7CDGXAQ',
                  'QHH7bIgA0BmEc4fUwdvGrNJvUuwWoD86N9zXZ4PH',tls=True)
            self.conn.upload(filename,f,'image-service-0528')
            self.wfile.write(filename)
            self.send_response(200,'OK')
            os.remove(filename)


server = HTTPServer(('', 18080), StoreHandler)
server.serve_forever()
