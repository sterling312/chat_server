#!/usr/bin/env python
import pdb
import argparse
import socket
try:
    from urllib2 import urlparse as parse
except ImportError:
    from urllib import parse
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, FallbackHandler
from tornado.wsgi import WSGIContainer
from tornado.websocket import WebSocketHandler

parser = argparse.ArgumentParser()
parser.add_argument('-p','--port',help='server port',default=8080)
parser.add_argument('--host',help='host ip',default=socket.gethostbyname(socket.gethostname()))

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('chat.html')

@app.route('/url')
def url():
    username = request.args.get('username','anonymous')
    url = parse.urlparse(request.url)
    url = 'ws://%(netloc)s/ws' % dict(netloc=url.netloc)
    return jsonify(url=url,username=username)

class WS(WebSocketHandler):
    cl = []
    def open(self):
        self.username = self.get_arguments('username')[0]
        if not self in self.cl:
            if self.authenticate():
                self.write_message('connected')
                self.broadcast(self.username+' logged in')
                self.cl.append(self)

    def broadcast(self,message):
        for cl in self.cl:
            cl.write_message(message)

    def on_message(self,msg):
        if not self.authenticated:
            return 
        self.broadcast(self.username+': '+msg)
        
    def on_close(self):
        if self in self.cl:
            self.cl.remove(self)
        self.broadcast(self.username+' left room')

    def authenticate(self):
        self.authenticated = True
        return self.authenticated

if __name__=="__main__":
    args = parser.parse_args()
    server = Application([(r'/ws',WS),
                          (r'/.*',FallbackHandler,dict(fallback=WSGIContainer(app)))])
    server.listen(args.port,address=args.host)
    print(args.host,args.port)
    IOLoop.instance().start()
