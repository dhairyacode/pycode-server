# server.py
from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Python execution server is running!"})

@app.route("/execute", methods=["POST"])
def execute():
    try:
        data = request.get_json()
        code = data.get("code", "")

        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode("utf-8"))
            temp_file_path = temp_file.name

        # Run the code safely with subprocess
        result = subprocess.run(
            ["python", temp_file_path],
            capture_output=True,
            text=True,
            timeout=5  # prevent infinite loops
        )

        # Clean up
        os.remove(temp_file_path)

        return jsonify({
            "output": result.stdout if result.stdout else result.stderr
        })

    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
