from server import Server 
from gui.gui import Gui

if __name__=="__main__":
    gui = Gui()
    server = Server('127.0.0.1','5000',gui)
    server.start()
    gui.run()
    