from flask import Flask, render_template, request, jsonify
import planner_logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/plan', methods=['POST'])
def plan_route_api():
    data = request.get_json()
    if not data or 'capacity' not in data:
        return jsonify({'error': 'Missing truck capacity'}), 400
    
    try:
        capacity = int(data['capacity'])
        if capacity <= 0: raise ValueError()
        results = planner_logic.plan_delivery(capacity)
        return jsonify(results)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected server error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)