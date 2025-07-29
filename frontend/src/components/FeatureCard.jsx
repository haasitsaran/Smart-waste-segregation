import React from 'react';
import { Link } from 'react-router-dom';
import { FiArrowRight } from 'react-icons/fi';

// The card now accepts an optional 'to' prop for routing
const FeatureCard = ({ icon, title, description, linkText, to }) => {
  // If a 'to' prop is provided, render a Link component from React Router
  if (to) {
    return (
      <Link to={to} className="bg-white p-6 rounded-xl border border-gray-200/80 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col">
        <div className="flex-grow">
          <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
            {icon}
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
          <p className="text-gray-600">{description}</p>
        </div>
        <div className="flex items-center mt-6 font-semibold text-green-600 hover:text-green-700">
          {linkText} <FiArrowRight className="ml-1" />
        </div>
      </Link>
    );
  }

  // Otherwise, render a non-clickable div with a button
  return (
    <div className="bg-white p-6 rounded-xl border border-gray-200/80 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col">
      <div className="flex-grow">
        <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-gray-800 mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
      <button className="flex items-center mt-6 font-semibold text-green-600 hover:text-green-700 cursor-pointer">
        {linkText} <FiArrowRight className="ml-1" />
      </button>
    </div>
  );
};

export default FeatureCard;
