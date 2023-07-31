from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def health_check():
    return "all good", 200

@app.route('/status_check')
def status_check():
    current_status = 'status_check'
    return jsonify({'current_status':current_status}),200
    
@app.route('/change_status')
def change_status():
    print('change_status')
    return "OK", 200

@app.route('/end_shift')
def end_shift():
    print('end_shift')
    return "OK",200

@app.route('/start_shift')
def start_shift():
    print('start_shift')
    return "OK",200

if __name__=="__main__":
    app.run(host='0.0.0.0', port="5000")