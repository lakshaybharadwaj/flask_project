from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "📱 Welcome to the Full Mobile Price Prediction API (Mock Version)"

@app.route('/predict/', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract inputs with fallbacks
        screen_size = float(data.get("screen_size", 6.5))
        rear_camera_mp = float(data.get("rear_camera_mp", 48))
        front_camera_mp = float(data.get("front_camera_mp", 16))
        internal_memory = int(data.get("internal_memory", 128))
        ram = float(data.get("ram", 6))
        battery = int(data.get("battery", 4500))
        weight = float(data.get("weight", 180))
        days_used = int(data.get("days_used", 300))
        new_price = float(data.get("normalized_new_price", 25000))
        device_brand = data.get("Device_Brand", "Samsung").lower()
        release_year = int(data.get("release_year", 2020))
        is_5g = data.get("5g", "no").lower()
        is_4g = data.get("4g", "yes").lower()

        # Mock scoring logic
        score = (
            screen_size * 300 +
            rear_camera_mp * 20 +
            front_camera_mp * 10 +
            internal_memory * 5 +
            ram * 100 +
            battery * 1 +
            (50 / weight) +
            (365 - days_used) * 2 +
            (new_price * 0.3)
        )

        if is_5g == "yes":
            score += 1500
        if is_4g == "yes":
            score += 500

        # Brand multiplier
        if device_brand == "apple":
            score *= 1.9
        elif device_brand == "samsung":
            score *= 1.4
        elif device_brand == "xiaomi":
            score *= 1.2
        elif device_brand == "realme":
            score *= 1.1
        else:
            score *= 1.0

        # Year decay penalty
        year_penalty = max(0, (2025 - release_year)) * 100
        score -= year_penalty

        return jsonify({
            "prediction": round(score, 2),
            "note": "Mock prediction using all fields"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
