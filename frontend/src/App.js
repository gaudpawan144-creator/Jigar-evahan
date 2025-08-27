import React, { useState } from 'react';
import './styles.css';

function App() {
  const [userName, setUserName] = useState('');
  const [fromPlace, setFromPlace] = useState('');
  const [toPlace, setToPlace] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/api/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_name: userName, from_place: fromPlace, to_place: toPlace })
    });
    const data = await res.json();
    setStatus(data.message);
    setUserName(''); setFromPlace(''); setToPlace('');
  }

  return (
    <div className="container">
      <h1>🛺 Book an E-Rickshaw</h1>
      <form onSubmit={handleSubmit} className="form">
        <input type="text" placeholder="Your Name" value={userName} onChange={(e)=>setUserName(e.target.value)} required />
        <input type="text" placeholder="From" value={fromPlace} onChange={(e)=>setFromPlace(e.target.value)} required />
        <input type="text" placeholder="To" value={toPlace} onChange={(e)=>setToPlace(e.target.value)} required />
        <button type="submit">Book E-Rickshaw</button>
      </form>
      {status && <p className="status">{status}</p>}
    </div>
  );
}

export default App;
