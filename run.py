import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import datetime

 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message('<b>Hi client, I will start to send values from sensor on every 2 sec</b>')
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=2), self.test)
      
    def on_message(self, message):
        if (message == ''):
            message = 'blank message'
        print 'message received: ', message
        self.write_message('Hey client, you sent me <b>'+message+'</b')
 
    def on_close(self):
        print 'connection closed'
 
    def check_origin(self, origin):
        return True
    
    def test(self):
        self.write_message("New value from sensor")
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=2), self.test)
 
application = tornado.web.Application([
    (r'/getValue', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    myIP = socket.gethostbyname(socket.gethostname())
    print 'Websocket Server Started at localhost:8000' 
    tornado.ioloop.IOLoop.instance().start()
