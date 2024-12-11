from flask import Flask, request, jsonify

api_key = "YOUR_API_KEY"

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

if __name__ == "__main__":
    app.run(debug=True)

