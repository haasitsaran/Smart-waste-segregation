import React, { useState, useEffect } from 'react';
import { FiClock, FiList, FiAlertTriangle } from 'react-icons/fi';

const History = () => {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/history');
        if (!response.ok) {
          throw new Error('Failed to fetch history data.');
        }
        const data = await response.json();
        setHistory(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []); // Empty dependency array means this runs once on component mount

  if (isLoading) {
    return <div className="text-center py-16">Loading history...</div>;
  }

  if (error) {
    return (
      <div className="container mx-auto px-6 py-16 text-center">
        <div className="max-w-md mx-auto bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center gap-3">
          <FiAlertTriangle className="w-6 h-6"/>
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <section className="container mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Detection History</h2>
      
      {history.length === 0 ? (
        <p className="text-center text-gray-500">No detection history found.</p>
      ) : (
        <div className="max-w-3xl mx-auto space-y-6">
          {history.map((record) => (
            <div key={record._id} className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
              <div className="flex justify-between items-center mb-4 border-b pb-3">
                <h3 className="font-bold text-lg text-gray-700">Detection Record</h3>
                <div className="flex items-center text-sm text-gray-500">
                  <FiClock className="mr-2" />
                  {/* Format the timestamp to be more readable */}
                  {new Date(record.timestamp).toLocaleString()}
                </div>
              </div>
              <div className="space-y-3">
                {record.detected_items.map((item, index) => (
                  <div key={index} className="p-3 bg-gray-50 rounded-lg">
                    <p className="font-semibold text-gray-800">{item.name} <span className="font-normal text-gray-500">({item.confidence}% confidence)</span></p>
                    <p className="text-sm text-teal-700">{item.binDescription}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default History;
