import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado import gen

import time

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self._break = False
        print "New client connected"
        self.write_message("You are connected")
        # tornado.ioloop.IOLoop.current().spawn_callback(self.send_values_from_sensor)
        self.send_values_from_sensor()
        
        
    # This is Real Time function. Explanation on bottom of page:
    # http://www.tornadoweb.org/en/stable/guide/coroutines.html
    @gen.coroutine
    def send_values_from_sensor(self):
        while True:
            if self._break:
                break
            nxt = gen.sleep(1) # Start the clock.
            yield self.send_message() # Run while the clock is ticking.
            yield nxt # Wait for the timer to run out.
    
    def send_message(self):
        time.sleep(0.9) # Simulate calculation
        return self.write_message('hi')
            
    def on_messagee(self, message):
        self.write_message(message)
        
    def on_close(self):
        self._break = True
        print "Client disconnected"
        
    def check_origin(self, origin):
        # allow_origin = self.server.settings.get("websocket_allow_origin", "*")
        # if allow_origin == "*":
        #     return True
        return True
    
    
application = tornado.web.Application([
    (r"/getValue", WebSocketHandler),
])

if __name__ == '__main__':
    application.listen(8000)
    print "Web socket server listen on localhost:8000"
    tornado.ioloop.IOLoop.instance().start()
