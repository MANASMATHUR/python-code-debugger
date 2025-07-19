from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)
CORS(app)  # Allow requests from React

def execute_code(code: str) -> str:
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return " Code executed successfully."
    except Exception:
        return f" Error:\n{traceback.format_exc()}"

def ask_groq_to_debug(code: str, error: str) -> str:
    prompt = f"""
You are a helpful AI programming assistant.

The following Python code has an error:

Code:
{code}

Error:
{error}

Please return only the fixed Python code. Do not include explanations.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

@app.route("/debug", methods=["POST"])
def debug_code():
    data = request.json
    code = data.get("code", "")
    result = execute_code(code)

    if "Error:" in result:
        fix = ask_groq_to_debug(code, result)
        return jsonify({"result": fix})
    else:
        return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
