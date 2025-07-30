import React from 'react';
import { FaRecycle, FaUserCircle } from 'react-icons/fa';
import { FiClock } from 'react-icons/fi';
import { Link, NavLink } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
      <nav className="container mx-auto px-6 py-3 flex justify-between items-center">
        {/* Logo and brand name link to the homepage */}
        <Link to="/" className="flex items-center space-x-2">
          <FaRecycle className="w-8 h-8 text-green-600" />
          <div className='flex flex-col'>
            <span className="text-xl font-bold text-gray-800">Code Crew</span>
            <span className="text-xs text-gray-500 -mt-1">Smart Waste Sorting</span>
          </div>
        </Link>
        <div className="flex items-center space-x-4">
          {/* History link */}
          <NavLink 
            to="/history" 
            className={({ isActive }) => 
              `flex items-center text-gray-600 hover:text-teal-600 ${isActive ? 'text-teal-600 font-bold' : ''}`
            }
          >
            <FiClock className="mr-1" />
            History
          </NavLink>
          <FaUserCircle className="w-8 h-8 text-gray-500 cursor-pointer" />
        </div>
      </nav>
    </header>
  );
};

export default Header;
