from flask import Flask, jsonify
import random
import requests

app = Flask(__name__)

def get_real_price():
    url = 'https://quotes.exness.com/quotes'
    params = {'symbols': 'XAUUSD'}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data['XAUUSD']['ask']
    except:
        return None

@app.route('/predict', methods=['GET'])
def predict():
    current_price = get_real_price()
    if current_price is None:
        return jsonify({'error': 'Không thể lấy giá'}), 500

    signal = random.choice(['BUY', 'SELL'])
    take_profit = current_price + 10 if signal == 'BUY' else current_price - 10
    stop_loss = current_price - 10 if signal == 'BUY' else current_price + 10

    return jsonify({
        'signal': signal,
        'take_profit': round(take_profit, 2),
        'stop_loss': round(stop_loss, 2),
        'current_price': round(current_price, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)