import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import './index.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} systemStatus="OPERATIONAL" />
      <Dashboard activeTab={activeTab} />
    </div>
  );
}
