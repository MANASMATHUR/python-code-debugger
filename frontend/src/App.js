import React, { useState } from 'react';
import './App.css';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { darcula, prism } from 'react-syntax-highlighter/dist/esm/styles/prism';

function App() {
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [fixedCode, setFixedCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [history, setHistory] = useState([]);

  const handleDebug = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/debug', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      const data = await response.json();
      setOutput('✅ Debugged successfully.');
      setFixedCode(data.result);
      setHistory(prev => [...prev, { input: code, output: data.result }]);
    } catch (err) {
      setOutput('❌ Error connecting to server.');
      setFixedCode('');
    }
    setLoading(false);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className={`app-container ${darkMode ? 'dark' : ''}`}>
      <header>
        <h1>CodeGPT Debug Assistant</h1>
        <p className="intro">Paste your Python code below and let AI fix your bugs instantly.</p>
        <button onClick={() => setDarkMode(!darkMode)} className="dark-toggle">
          {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
        </button>
      </header>

      <div className="instructions">
        <h2> How it works:</h2>
        <ul>
          <li>✅ Paste broken Python code</li>
          <li>🛠️ Click <strong>Debug Code</strong></li>
          <li>📜 View and copy the fixed version</li>
        </ul>
      </div>

      <textarea
        className="code-input"
        placeholder="Paste your Python code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      ></textarea>

      <button className="run-button" onClick={handleDebug} disabled={loading}>
        {loading ? ' Debugging...' : '🛠️ Debug Code'}
      </button>

      {output && (
        <div className="output">
          <h3>Execution Result:</h3>
          <SyntaxHighlighter language="text" style={darkMode ? darcula : prism}>
            {output}
          </SyntaxHighlighter>
          <button onClick={() => copyToClipboard(output)}> Copy Output</button>
        </div>
      )}

      {fixedCode && (
        <div className="fixed-code">
          <h3>AI-Suggested Fix:</h3>
          <SyntaxHighlighter language="python" style={darkMode ? darcula : prism}>
            {fixedCode}
          </SyntaxHighlighter>
          <button onClick={() => copyToClipboard(fixedCode)}> Copy Fix</button>
        </div>
      )}

      {history.length > 0 && (
        <div className="history">
          <h3> Debug History:</h3>
          {history.map((entry, index) => (
            <div key={index} className="history-entry">
              <p><strong>Input:</strong></p>
              <SyntaxHighlighter language="python" style={darkMode ? darcula : prism}>
                {entry.input}
              </SyntaxHighlighter>
              <p><strong>Output:</strong></p>
              <SyntaxHighlighter language="python" style={darkMode ? darcula : prism}>
                {entry.output}
              </SyntaxHighlighter>
              <hr />
            </div>
          ))}
        </div>
      )}

      
    </div>
  );
}

export default App;
