import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.web
import json
import time
import os

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), 'static'),
    "static_url_prefix": "/static/",
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        MainHandler.render(self,"templates/main.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    def open(self):
        #name=tornado.websocket.WebSocketHandler.get_body_argument(self,'a')
        #self.write_message(u"Name: "+name)
        #print(name)
        SocketHandler.clients.add(self)
        print("User connected!")
        msg=json.dumps({'event':'connect', 'user':'User'})
        self.send(msg)

    def check_origin(self, origin):
        return True

    def send(self, message):
        for client in SocketHandler.clients:
            client.write_message(json.dumps(message))

    def on_message(self, message):
        print(json.loads(message))
        if json.loads(message)['event']=='message':
           msg={'event':'message', 'message':json.loads(message)['message']}
           self.send(msg)
        elif json.loads(message)['event']=='register':
            pass


    def on_close(self):
        SocketHandler.clients.remove(self)
        print("Connection closed")

application = tornado.web.Application([
    (r"/", SocketHandler),
    (r"/chat", MainHandler),
], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.instance().start()
