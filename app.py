from flask import Flask, request, render_template
import requests

app = Flask(__name__, static_url_path='/static')

# Define TONCenter API here
API_KEY = "TON_CENTER_API_HERE"

# Home Page
@app.route('/')
def index():
    ton_price_data = get_ton_price()
    return render_template('index.html', ton_price_data=ton_price_data)

# Search Function
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    data = query_ton_network(query)
    ton_price_data = get_ton_price()
    return render_template('results.html', data=data, ton_price_data=ton_price_data)

# Address query function of the TON network
def query_ton_network(query):
    api_url = f"https://toncenter.com/api/v2/getAddressInformation?address={query}"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'result' in data:
            result = data['result']
            if 'balance' in result:
                result['balance'] = float(result['balance']) / 10 ** 9  # Converting Balance value to TON format
            # Address bilgisini ekleyelim
            result['address'] = query
            return result
        else:
            return {"error": "Data not found"}
    else:
        return {"error": "Data not found"}

# Function to fetch TON price and market cap
def get_ton_price():
    api_url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd&include_market_cap=true"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'the-open-network' in data:
            ton_data = data['the-open-network']
            return {
                'price': ton_data['usd'],
                'market_cap': ton_data['usd_market_cap']
            }
        else:
            return {"error": f"Data not found: {data}"}
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}

if __name__ == '__main__':
    app.run(debug=True)
