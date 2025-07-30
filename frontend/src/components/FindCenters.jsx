import React, { useState, useEffect } from 'react';
import { FiMapPin, FiAlertTriangle, FiInfo, FiExternalLink } from 'react-icons/fi';

const FindCenters = () => {
  const [suggestions, setSuggestions] = useState([]);
  const [detectedTypes, setDetectedTypes] = useState([]);
  const [allCenters, setAllCenters] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/recycling-centers');
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch suggestions.');
        }
        setSuggestions(data.suggestions);
        setDetectedTypes(data.detected_types);
        setAllCenters(data.all_centers);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchSuggestions();
  }, []);

  const CenterCard = ({ center }) => (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 flex flex-col">
        <div className="flex-grow">
            <h4 className="font-bold text-lg text-gray-800">{center.name}</h4>
            <p className="text-gray-600 my-2 flex items-start">
                <FiMapPin className="w-4 h-4 mr-2 mt-1 flex-shrink-0"/>
                {center.address}
            </p>
            <div className="mt-4">
                <p className="text-sm font-semibold text-gray-700">Accepts:</p>
                <div className="flex flex-wrap gap-2 mt-2">
                    {center.accepts.map(item => <span key={item} className="text-xs bg-gray-200 text-gray-800 px-2 py-1 rounded-full">{item}</span>)}
                </div>
            </div>
        </div>
        <a 
            href={center.url} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="mt-4 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-teal-700 bg-teal-100 hover:bg-teal-200"
        >
            View on Map <FiExternalLink className="ml-2 h-4 w-4" />
        </a>
    </div>
  );

  return (
    <section className="container mx-auto px-6 py-16">
      <div className="max-w-3xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Find Nearby Recycling Centers</h2>
        <p className="text-gray-600 mb-12">
          Based on your recent scans, here are some suggested recycling centers. You can also browse all available locations.
        </p>
      </div>

      {isLoading && <div className="text-center text-lg font-semibold">Finding suggestions...</div>}
      {error && (
        <div className="max-w-md mx-auto bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center gap-3">
          <FiAlertTriangle className="w-6 h-6"/>
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {!isLoading && !error && (
        <div className="max-w-4xl mx-auto space-y-12">
          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Suggestions for You</h3>
            {detectedTypes.length > 0 && (
                 <div className="mb-6 p-4 bg-teal-50 border border-teal-200 rounded-lg flex items-start space-x-3">
                    <FiInfo className="w-5 h-5 text-teal-600 mt-1 flex-shrink-0"/>
                    <p className="text-sm text-teal-800">
                        Suggestions are based on your recent detections of: <span className="font-semibold">{detectedTypes.join(', ')}</span>.
                    </p>
                </div>
            )}
            {suggestions.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {suggestions.map(center => <CenterCard key={center.id} center={center} />)}
              </div>
            ) : (
              <p className="text-center text-gray-500">No specific suggestions based on your recent history. Try scanning some items!</p>
            )}
          </div>

          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">All Recycling Centers</h3>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {allCenters.map(center => <CenterCard key={center.id} center={center} />)}
              </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default FindCenters;
