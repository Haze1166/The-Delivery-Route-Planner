# app.py
from flask import Flask, render_template, request, jsonify
import planner_logic

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/api/plan', methods=['POST'])
def plan_route_api():
    """API endpoint to handle the planning request."""
    data = request.get_json()
    if not data or 'capacity' not in data:
        return jsonify({'error': 'Missing truck capacity'}), 400
    
    try:
        capacity = int(data['capacity'])
        if capacity <= 0:
            raise ValueError()
            
        results = planner_logic.plan_delivery(capacity)
        
        if results.get('error'):
            return jsonify(results), 400 # Bad request if there's a logical error
            
        return jsonify(results)

    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid capacity. Please enter a positive whole number.'}), 400
    except FileNotFoundError:
        return jsonify({'error': 'Server configuration error: Data file not found.'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}") # Log the error for debugging
        return jsonify({'error': 'An unexpected server error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)