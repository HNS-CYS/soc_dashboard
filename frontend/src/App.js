import React, { useState } from 'react';
import './App.css';

const SERVICES = [
  { id: 'wazuh', name: 'Wazuh', url: '/proxy/wazuh/', icon: '🛡️' },
  { id: 'shuffle', name: 'Shuffle', url: '/proxy/shuffle/', icon: '🔀' },
  { id: 'iris', name: 'DFIR-IRIS', url: '/proxy/iris/', icon: '🔍' },
  { id: 'velociraptor', name: 'Velociraptor', url: '/proxy/velociraptor/', icon: '🦖' }
];

function App() {
  const [activeService, setActiveService] = useState(SERVICES[0]);
  const [loading, setLoading] = useState(true);

  const handleServiceChange = (service) => {
    setLoading(true);
    setActiveService(service);
  };

  const handleIframeLoad = () => {
    setLoading(false);
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>🔐 SOC Dashboard</h1>
        </div>
        
        <nav className="sidebar-nav">
          {SERVICES.map((service) => (
            <button
              key={service.id}
              className={`nav-item ${activeService.id === service.id ? 'active' : ''}`}
              onClick={() => handleServiceChange(service)}
            >
              <span className="nav-icon">{service.icon}</span>
              <span className="nav-label">{service.name}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <p>v1.0.0</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="content-header">
          <h2>{activeService.name}</h2>
          <div className="header-actions">
            <button 
              className="btn-refresh"
              onClick={() => {
                setLoading(true);
                document.getElementById('service-iframe').src = activeService.url;
              }}
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        <div className="iframe-container">
          {loading && (
            <div className="loading-overlay">
              <div className="spinner"></div>
              <p>Loading {activeService.name}...</p>
            </div>
          )}
          <iframe
            id="service-iframe"
            src={activeService.url}
            title={activeService.name}
            onLoad={handleIframeLoad}
            onError={() => setLoading(false)}
          />
        </div>
      </main>
    </div>
  );
}

export default App;