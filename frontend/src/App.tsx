import React, { useState, useEffect } from 'react';
import './App.css';

interface Camera {
  id: string;
  name: string;
  url: string;
  isStreaming: boolean;
}

function App() {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchCameras = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('http://localhost:5000/api/cameras');
      if (!response.ok) {
        throw new Error('Failed to load cameras');
      }
      const data = await response.json();
      setCameras(data);
    } catch (err) {
      setError('Failed to load cameras. Please try again later.');
      console.error('Error fetching cameras:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCameras();
  }, []);

  const toggleStream = async (cameraId: string) => {
      const camera = cameras.find((c: Camera) => c.id === cameraId);
    try {
      if (!camera) return;

      const newStatus = !camera.isStreaming;
      const response = await fetch(`http://localhost:5000/api/cameras/${cameraId}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ isStreaming: newStatus })
      });

      if (!response.ok) {
        throw new Error('Failed to toggle stream');
      }

      setCameras(cameras.map((c: Camera) => 
        c.id === cameraId ? { ...c, isStreaming: newStatus } : c
      ));
    } catch (err) {
      setError(`Failed to ${camera?.isStreaming ? 'stop' : 'start'} stream. Please try again.`);
      console.error('Error toggling stream:', err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MJPG Streamer Web</h1>
        <button className="refresh-button" onClick={fetchCameras}>
          ↻
        </button>
      </header>

      <main className="App-content">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Loading...
          </div>
        ) : cameras.length === 0 ? (
          <div className="no-cameras">
            No cameras available
          </div>
        ) : (
          <div className="camera-grid">
            {cameras.map((camera: Camera) => (
              <div key={camera.id} className="camera-card">
                <h2 className="camera-title">{camera.name}</h2>
                <div className="camera-feed">
                  {camera.isStreaming ? (
                    <img 
                      src={`http://localhost:5000/api/cameras/${camera.id}/stream`}
                      alt={`Stream from ${camera.name}`}
                    />
                  ) : (
                    <div className="stream-stopped">
                      Stream stopped
                    </div>
                  )}
                </div>
                <div className="camera-controls">
                  <button 
                    className={`stream-button ${camera.isStreaming ? 'stop' : 'start'}`}
                    onClick={() => toggleStream(camera.id)}
                  >
                    {camera.isStreaming ? 'Stop' : 'Start'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
