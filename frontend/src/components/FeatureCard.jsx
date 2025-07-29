import React from 'react';
import { FiArrowRight } from 'react-icons/fi';

const FeatureCard = ({ icon, title, description, linkText }) => {
  return (
    <div className="bg-white p-6 rounded-xl border border-gray-200/80 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col">
      <div className="flex-grow">
        <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
      <a href="#" className="flex items-center mt-6 font-semibold text-green-600 hover:text-green-700">
        {linkText} <FiArrowRight className="ml-1" />
      </a>
    </div>
  );
};

export default FeatureCard;