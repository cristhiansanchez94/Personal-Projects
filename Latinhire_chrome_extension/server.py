import threading 
from api import Flask_api


class Server(threading.Thread):
    def __init__(self, host, port, gui):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.gui = gui
        self.daemon = True
        self.app = Flask_api(gui).get_app()
    
    def run(self):     
        print(f"Listening on http://{self.host}:{self.port}\n")
        self.app.run(host=self.host, port=self.port, debug=True, use_reloader=False)