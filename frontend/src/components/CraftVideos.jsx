import React, { useState, useEffect } from 'react';
import { FiYoutube, FiAlertTriangle } from 'react-icons/fi';

const CraftVideos = () => {
  const [craftIdeas, setCraftIdeas] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCraftIdeas = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5001/api/craft-ideas');
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch craft ideas.');
        }
        setCraftIdeas(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchCraftIdeas();
  }, []);

  return (
    <section className="container mx-auto px-6 py-16">
      <div className="max-w-3xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Upcycle & Craft Ideas</h2>
        <p className="text-gray-600 mb-12">
          Get inspired to turn your waste into something wonderful! Here are some creative ideas based on your most recently detected item.
        </p>
      </div>

      {isLoading && <div className="text-center text-lg font-semibold">Generating creative ideas...</div>}
      {error && (
        <div className="max-w-md mx-auto bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center gap-3">
          <FiAlertTriangle className="w-6 h-6"/>
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {!isLoading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {craftIdeas.map((idea, index) => (
            <div key={index} className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
              <div className="p-6">
                <span className="text-sm font-semibold text-teal-600 bg-teal-100 px-3 py-1 rounded-full">
                  {idea.wasteType}
                </span>
                <h3 className="text-xl font-bold text-gray-800 mt-4 mb-2">{idea.title}</h3>
                <p className="text-gray-600 mb-4">{idea.description}</p>
                <a
                  href={`https://www.youtube.com/watch?v=${idea.videoId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center font-semibold text-red-600 hover:text-red-700"
                >
                  <FiYoutube className="mr-2" />
                  Watch on YouTube
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default CraftVideos;
