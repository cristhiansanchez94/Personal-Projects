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
        
        @self.app.route('/missed_session')
        def missed_session():
            if self.gui.running:
                self.gui.event_generate("<<MissedSession>>", when='tail')
                return "OK",200
            else: 
                return "App was not running", 200
            
        @self.app.route('/change_status')
        def change_status():
            if self.gui.running:
                self.gui.event_generate("<<StatusChanged>>", when='tail')
                return "Changed status", 200
            else:
                return "App was not running", 200
        
        @self.app.route('/end_shift')
        def end_shift():
            if self.gui.running:
                if self.gui.general_counter>=self.gui.counter+2*60*60:
                    self.gui.event_generate("<<EndShift>>", when='tail')
                    return "Shift ended",200
                else: 
                    self.gui.event_generate("<<EndShiftUnexp>>", when='tail')
                    return "Shift ended unexpectedly", 200
            return "App was not running", 200
        
        @self.app.route('/start_shift')
        def start_shift():
            if not self.gui.running:
                self.gui.event_generate("<<StartShift>>", when='tail')
                return "Shift started",200
            return "App was not running", 200

    def get_app(self):
        return self.app


