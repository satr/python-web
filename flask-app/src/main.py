import http

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def root():
    return "root"

@app.route("/healthz")
def healthz():
    return "OK", http.HTTPStatus.OK

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8001)