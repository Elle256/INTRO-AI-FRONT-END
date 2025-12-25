import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [text, setText] = useState('');
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/summarize', {
        text: text,
        num_sentences: 3
      });
      setSummary(res.data.summary);
    } catch (err) {
      alert("Lỗi kết nối Backend!");
    }
    setLoading(false);
  };

  return (
    <div style={{ 
    background: 'radial-gradient(circle, rgba(238, 174, 202, 1) 0%, rgba(148, 187, 233, 1) 100%)', 
    minHeight: '100vh', 
    minWidth: '100vw',
    display: 'flex', 
    justifyContent: 'center', 
    padding: '20px'
  }}>
    <div style={{ 
      padding: '40px',  
      width: '100%',
      height: '90%',
      backgroundColor: 'rgba(250,250,250,0.6)', 
      borderRadius: '15px', 
      boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
      textAlign: 'center' 
    }}>
      <h1 style={{ color: '#333' }}>AI Text Summarizer</h1>
      <textarea
        rows="10"
        style={{ 
          width: '100%', 
          padding: '15px', 
          borderRadius: '8px', 
          border: '1px solid #0b0b0bff',
          boxSizing: 'border-box' 
        }}
        placeholder="Dán văn bản vào đây..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <br />
      <button 
        onClick={handleSummarize} 
        disabled={loading || !text}
        style={{ 
          marginTop: '20px', 
          padding: '15px', 
          cursor: 'pointer',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
          color: '#fff', 
          border: 'none',
          borderRadius: '25px',
          fontWeight: 'bold',
          width: '100%'
        }}
      >
        {loading ? 'Đang tóm tắt...' : 'Tóm tắt ngay'}
      </button>

      {summary.length > 0 && (
        <div style={{ 
          marginTop: '25px', 
          backgroundColor: '#f9f9f9', 
          padding: '20px', 
          paddingRight: '25px',
          borderRadius: '20px',
          textAlign: 'left',
          width: '100%',
          boxSizing: 'border-box',
          minHeight: '100px',
        }}>
          <h3 style={{ color: '#764ba2' }}>Kết quả:</h3>
          <ul style={{ lineHeight: '1.6' }}>
            {summary.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}
    </div>
  </div>
  );
}

export default App;