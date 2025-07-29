import React, { useState, useRef } from 'react';
import { FiCamera, FiMaximize, FiCheckCircle, FiAlertTriangle, FiVideo, FiVideoOff } from 'react-icons/fi';
import { FaRecycle } from 'react-icons/fa';

const Scanner = () => {
  const [scanResult, setScanResult] = useState([]);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [scanAttempted, setScanAttempted] = useState(false);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const handleToggleCamera = async () => {
    if (isCameraOn) {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      setIsCameraOn(false);
      setScanResult([]);
      setError(null);
      setScanAttempted(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: 'environment' }
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        streamRef.current = stream;
        setIsCameraOn(true);
        setError(null);
      } catch (err) {
        console.error("Error accessing camera:", err);
        setError("Could not access the camera. Please check permissions and try again.");
      }
    }
  };

  const handleDetect = () => {
    if (!isCameraOn) {
      setError("Please start the camera first.");
      return;
    }
    
    setIsScanning(true);
    setScanResult([]);
    setError(null);
    setScanAttempted(true);

    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      try {
        const response = await fetch('http://127.0.0.1:5000/api/detect', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const result = await response.json();

        // --- FIX: Check if the result is an array before setting state ---
        if (Array.isArray(result)) {
            setScanResult(result);
        } else if (result.error) {
            // If the backend sent an error object, display it
            setError(result.error);
        } else {
            // Handle any other unexpected response
            throw new Error("Received an unexpected data format from the server.");
        }

      } catch (err) {
        console.error("Error during detection:", err);
        setError("Could not analyze the image. Is the Python server running correctly?");
      } finally {
        setIsScanning(false);
      }
    }, 'image/jpeg');
  };

  return (
    <section className="container mx-auto px-6 py-16 flex flex-col items-center space-y-8">
      <div className="w-full max-w-lg aspect-[4/3] bg-black rounded-2xl flex justify-center items-center text-gray-600 relative overflow-hidden">
        <video ref={videoRef} autoPlay playsInline className={`w-full h-full object-cover ${!isCameraOn && 'hidden'}`}></video>
        {!isCameraOn && <FiMaximize className="w-16 h-16 opacity-50" />}
        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
        <div className="absolute inset-0 border-4 border-white/20 rounded-2xl pointer-events-none"></div>
        {isCameraOn && (
          <span className="absolute top-4 right-4 bg-red-500 text-white px-3 py-1 text-sm font-bold rounded-full flex items-center gap-2">
              <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
              LIVE
          </span>
        )}
      </div>
      
      <div className="flex items-center space-x-4">
        <button 
          onClick={handleToggleCamera}
          className={`flex items-center space-x-2 font-bold px-6 py-3 rounded-lg shadow-lg transition-colors ${isCameraOn ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-green-500 hover:bg-green-600 text-white'}`}
        >
          {isCameraOn ? <FiVideoOff /> : <FiVideo />}
          <span>{isCameraOn ? 'Stop Camera' : 'Start Camera'}</span>
        </button>
        <button 
          onClick={handleDetect} 
          disabled={!isCameraOn || isScanning}
          className="bg-amber-400 text-amber-900 font-bold px-8 py-3 rounded-lg shadow-lg hover:bg-amber-500 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <FiCamera />
          <span>{isScanning ? 'Analyzing...' : 'Detect Waste'}</span>
        </button>
      </div>

      {error && (
        <div className="w-full max-w-lg bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative flex items-center gap-3">
            <FiAlertTriangle className="w-6 h-6"/>
            <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="w-full max-w-lg space-y-4">
        {scanResult.length > 0 && (
          <>
            <h3 className="text-2xl font-bold text-center">Detection Results</h3>
            {scanResult.map((result, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-xl shadow-md p-6 animate-fade-in-up">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center space-x-3">
                    <FiCheckCircle className="w-6 h-6 text-green-500" />
                    <div>
                      <h3 className="font-bold text-lg text-gray-800">{result.name}</h3>
                      <p className="text-sm text-gray-500">{result.confidence}% confidence</p>
                    </div>
                  </div>
                  <span className="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-1 rounded-full">Detected</span>
                </div>
                <div className="bg-green-100 text-green-900 p-4 rounded-lg flex items-center space-x-3 my-4">
                  <FaRecycle className="w-5 h-5 text-blue-500" />
                  <span className="font-medium">{result.binDescription}</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">🌿 Eco Tips</h4>
                  <ul className="list-disc list-inside text-gray-600 space-y-1">
                    {result.tips.map((tip, tipIndex) => <li key={tipIndex}>{tip}</li>)}
                  </ul>
                </div>
              </div>
            ))}
          </>
        )}

        {!isScanning && scanAttempted && scanResult.length === 0 && !error && (
          <div className="bg-white border border-gray-200 rounded-xl shadow-md p-6 animate-fade-in-up">
            <div className="flex items-center space-x-3">
              <FiAlertTriangle className="w-6 h-6 text-amber-500" />
              <div>
                <h3 className="font-bold text-lg text-gray-800">No Recognizable Waste Detected</h3>
                <p className="text-sm text-gray-500">Please try again with a clearer image.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default Scanner;
