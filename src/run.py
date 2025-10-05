from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from app import Api
import os

# Get the directory where flask_app.py is located (src/)
basedir = os.path.abspath(os.path.dirname(__file__))
# Go up one level to get to Meteor-Madness/
root_dir = os.path.dirname(basedir)

app = Flask(__name__,
            static_folder=os.path.join(root_dir, 'web'),
            template_folder=os.path.join(root_dir, 'web'),
            static_url_path='')

CORS(app)
api_handler = Api()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_asteroid_list', methods=['GET'])
def get_asteroid_list():
    result = api_handler.get_asteroid_list()
    return result, 200, {'Content-Type': 'application/json'}

@app.route('/api/run_simulation', methods=['POST'])
def run_simulation():
    data = request.json
    result = api_handler.run_simulation(
        asteroid_name=data.get('asteroid_name'),
        diameter=data.get('diameter'),
        velocity=data.get('velocity'),
        lat=data.get('lat'),
        long=data.get('long'),
        h_value=data.get('h_value'),
        v_inf_value=data.get('v_inf_value')
    )
    return result, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Meteor Madness Flask Server Starting...")
    print("🌐 Open http://127.0.0.1:5000 in your browser")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)