import React from 'react';
import { FaRecycle, FaUserCircle } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
      <nav className="container mx-auto px-6 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <FaRecycle className="w-8 h-8 text-green-600" />
          <div className='flex flex-col'>
            <span className="text-xl font-bold text-gray-800">Code Crew</span>
            <span className="text-xs text-gray-500 -mt-1">Smart Waste Sorting</span>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button className="px-4 py-2 border border-blue-300 bg-blue-50 rounded-full text-blue-700 font-semibold text-sm hover:bg-blue-100 transition">
            1,247 pts
          </button>
          <FaUserCircle className="w-8 h-8 text-gray-500 cursor-pointer" />
        </div>
      </nav>
    </header>
  );
};

export default Header;