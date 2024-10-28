from flask import Flask, render_template, request, jsonify
from config import load_config
from routes import load_routes
from utils import find_best_path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    mf_config = load_config('C:/Users/ASUS/Desktop/Millennium_falcon/data/millennium-falcon.json')
    autonomy = mf_config.get('autonomy', 0)  
    routes = load_routes(mf_config['routes_db'])

    
    data = request.get_json()

    if 'countdown' not in data or 'bounty_hunters' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    countdown = data['countdown']
    bounty_hunters = data['bounty_hunters']

    
    probability = find_best_path(routes, countdown, bounty_hunters, autonomy)

    return jsonify({"probability": probability})

if __name__ == "__main__":
    app.run(debug=True,port=5000)