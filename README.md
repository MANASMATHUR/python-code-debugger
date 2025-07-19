#  Python Code Debugger

A fullstack web app that helps debug Python code using Large Language Models (LLMs). Just paste your code, and get structured suggestions, fixes, and explanations. Built with a Flask backend and a React frontend.



## What It Does

- Accepts raw Python code from the user
- Sends it to a backend powered by an LLM (e.g., LLaMA 3 via Groq API)
- Returns:
  - The original code
  - Detected issues
  - Suggested fixes
  - Optional explanation



##  Tech Stack

- **Frontend**: React (Vite)
- **Backend**: Flask (Python)
- **LLM API**: Groq (OpenAI-compatible)
- **Parsing**: Python `ast` module



##  Project Structure

python-code-debugger/
│
├── frontend/ # React frontend
├── main.py # Optional script or entrypoint
├── server.py # Flask backend (API logic)
├── requirements.txt # Python dependencies
├── debug_log.txt # Log file for backend debugging
├── .env # API keys (not committed)
└── .gitignore



---

##  How to Run Locally

### 
1.Clone the repo
```bash
git clone https://github.com/MANASMATHUR/python-code-debugger.git
cd python-code-debugger

2. Set up your .env file
Create a .env file in the root directory:

env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama3-8b-8192

3. Start the backend
pip install -r requirements.txt
python server.py
Runs on: http://localhost:5000

4. Start the frontend
cd frontend
npm install
npm run dev
