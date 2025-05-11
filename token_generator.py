from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Zerodha API credentials - Store these in Render's environment variables
API_KEY = os.getenv('ZERODHA_API_KEY')
API_SECRET = os.getenv('ZERODHA_API_SECRET')
REDIRECT_URL = os.getenv('ZERODHA_REDIRECT_URL')  # Should match the one in Kite developer console

@app.route('/generate_access_token', methods=['GET'])
def generate_access_token():
    """
    Generate access token from request token
    Example request: /generate_access_token?request_token=xxxxxxxxxx
    """
    request_token = request.args.get('request_token')
    
    if not request_token:
        return jsonify({'error': 'Request token is required'}), 400
    
    try:
        # Step 1: Get session data from Zerodha
        session_url = "https://api.kite.trade/session/token"
        data = {
            "api_key": API_KEY,
            "request_token": request_token,
            "checksum": hashlib.sha256(f"{API_KEY}{request_token}{API_SECRET}".encode()).hexdigest()
        }
        
        response = requests.post(session_url, data=data)
        response.raise_for_status()
        
        session_data = response.json()
        
        # Step 2: Extract access token
        access_token = session_data['data']['access_token']
        
        # Store the token securely (in a real app, you'd use a database)
        token_data = {
            'access_token': access_token,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'data': token_data
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': f"Failed to generate access token: {str(e)}"
        }), 500
    except KeyError:
        return jsonify({
            'status': 'error',
            'message': 'Invalid response from Zerodha API'
        }), 500

@app.route('/')
def health_check():
    return jsonify({'status': 'running', 'service': 'zerodha_token_generator'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
