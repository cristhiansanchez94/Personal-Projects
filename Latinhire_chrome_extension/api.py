from flask import Flask, jsonify

class Flask_api():
    def __init__(self, gui): 
        self.app = Flask(__name__)
        self.build_app()
        self.gui = gui
        
    def build_app(self):
        @self.app.route('/')
        def default():
            return "OK", 200
        
        @self.app.route('/status_check')
        def status_check():
            current_status = self.gui.current_status
            return jsonify({'current_status':current_status}),200
            
        @self.app.route('/change_status')
        def change_status():
            self.gui.event_generate("<<StatusChanged>>", when='tail')
            return "OK", 200
        
        @self.app.route('/end_shift')
        def end_shift():
            self.gui.event_generate("<<EndShift>>", when='tail')
            return "OK",200
        
        @self.app.route('/start_shift')
        def start_shift():
            self.gui.event_generate("<<StartShift>>", when='tail')
            return "OK",200

    def get_app(self):
        return self.app

