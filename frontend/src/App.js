// frontend/src/App.js
import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [upscaledImage, setUpscaledImage] = useState(null);
  const [cartoonImage, setCartoonImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cartoonLoading, setCartoonLoading] = useState(false);
  const fileInputRef = useRef();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUpscaledImage(null);
    setCartoonImage(null);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
      setUpscaledImage(null);
      setCartoonImage(null);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const uploadImage = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setCartoonImage(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/upscale', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.error) {
        alert('Error: ' + data.error);
      } else {
        setUpscaledImage('data:image/png;base64,' + data.image);
      }
    } catch (error) {
      alert('Upload failed: ' + error.message);
    }

    setLoading(false);
  };

  const cartoonify = async () => {
    if (!upscaledImage) return;
    setCartoonLoading(true);

    // convert base64 back to Blob
    const base64 = upscaledImage.split(',')[1];
    const blob = b64toBlob(base64, 'image/png');

    const formData = new FormData();
    formData.append('image', blob, 'upscaled.png');

    try {
      const response = await fetch('http://localhost:5000/cartoonify', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }
      setCartoonImage('data:image/png;base64,' + data.image);
    } catch (error) {
      alert('Cartoonify failed: ' + error.message);
    }

    setCartoonLoading(false);
  };

  // helper for base64 → Blob
  function b64toBlob(b64Data, contentType = '', sliceSize = 512) {
    const byteChars = atob(b64Data);
    const byteArrays = [];
    for (let offset = 0; offset < byteChars.length; offset += sliceSize) {
      const slice = byteChars.slice(offset, offset + sliceSize);
      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      byteArrays.push(new Uint8Array(byteNumbers));
    }
    return new Blob(byteArrays, { type: contentType });
  }

  return (
    <div className="PageWrapper">
      <div className="App">
        <h1>🔍 Sharpify – AI Image Enhancer & Cartoonizer</h1>

        <div
          className={`upload-area${selectedFile ? ' selected' : ''}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => fileInputRef.current.click()}
        >
          <p>
            {selectedFile
              ? selectedFile.name
              : 'Click or Drag & Drop Image Here'}
          </p>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
        </div>

        <button onClick={uploadImage} disabled={!selectedFile || loading}>
          {loading ? 'Upscaling...' : 'Upscale Image'}
        </button>

        {loading && <div className="spinner"></div>}

        {upscaledImage && (
          <div className="result-container">
            <h2>Upscaled (×4)</h2>
            <img src={upscaledImage} alt="Upscaled result" />

            <button
              onClick={cartoonify}
              disabled={cartoonLoading}
              style={{ marginTop: '1em' }}
            >
              {cartoonLoading ? 'Cartoonifying...' : 'Cartoonify'}
            </button>
          </div>
        )}

        {cartoonImage && (
          <div className="result-container">
            <h2>Cartoonized</h2>
            <img src={cartoonImage} alt="Cartoon result" />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
