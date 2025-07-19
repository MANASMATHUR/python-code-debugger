import traceback
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to get multi-line input from the user
def get_multiline_input(prompt=">>> "):
    print("Enter your Python code (press Enter twice to finish):")
    lines = []
    while True:
        line = input(prompt)
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

# Function to execute user code safely
def execute_code(code: str) -> str:
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return " Code executed successfully."
    except Exception:
        return f" Error:\n{traceback.format_exc()}"

# Function to call Groq to debug broken code
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

# Function to log the session
def log_debug_session(original_code, error_message, fixed_code):
    with open("debug_log.txt", "a") as log_file:
        log_file.write("=== DEBUG SESSION ===\n")
        log_file.write("Original Code:\n")
        log_file.write(original_code + "\n\n")
        log_file.write("Error:\n")
        log_file.write(error_message + "\n\n")
        log_file.write("Suggested Fix:\n")
        log_file.write(fixed_code + "\n")
        log_file.write("=" * 40 + "\n\n")

# Main interface
def main():
    print(" Welcome to CodeGPT Debug Assistant!\n")
    user_code = get_multiline_input()

    print("\n Executing your code...\n")
    result = execute_code(user_code)
    print(result)

    if "Error:" in result or "X" in result:
        print("\n🛠 Sending error to Groq for debugging...\n")
        fixed_code = ask_groq_to_debug(user_code, result)
        print("\n Suggested Fix:\n")
        print(fixed_code)

        # Log session
        log_debug_session(user_code, result, fixed_code)

if __name__ == "__main__":
    main()

