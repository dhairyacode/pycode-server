from flask import Flask, request, jsonify
import sys
import io

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Python execution server is running!"})

@app.route("/run", methods=["POST"])
def run_code():
    try:
        code = request.json.get("code", "")
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        exec(code, {})
        sys.stdout = old_stdout
        return jsonify({"output": mystdout.getvalue()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
