import React from 'react';
import { FiArrowRight, FiCamera } from 'react-icons/fi';
import phoneMockup from '../assets/image.png'; // This path should now be correct

const Hero = () => {
  return (
    <section className="container mx-auto px-6 py-16 md:py-24 overflow-hidden ">
      {/* Main Grid Container: 1 column on mobile, 2 on large screens */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        
        {/* ---- Left Column: Text Content ---- */}
        <div className="flex flex-col space-y-6 text-center lg:text-left items-center lg:items-start">
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-800 leading-tight">
            Sort Waste <br /> Smarter
          </h1>
          <p className="text-lg text-gray-600 max-w-lg">
            Use your camera to instantly identify waste types and get disposal guidance. Make recycling effortless with AI-powered assistance.
          </p>
          <div className="flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4 pt-4">
            <button className="flex items-center justify-center bg-teal-500 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-teal-600 transition duration-300 w-full sm:w-auto">
              <FiCamera className="mr-2" /> Start Scanning
            </button>
            <button className="text-teal-600 font-semibold px-6 py-3 rounded-lg hover:bg-teal-50 transition duration-300 flex items-center">
              Learn More <FiArrowRight className="ml-1" />
            </button>
          </div>
          <div className="flex items-center space-x-12 pt-8">
            <div>
              <p className="text-3xl font-bold text-teal-600">80%+</p>
              <p className="text-gray-500">Accuracy</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-teal-600">2.3M</p>
              <p className="text-gray-500">Items Sorted</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-teal-600">50K</p>
              <p className="text-gray-500">Users</p>
            </div>
          </div>
        </div>
        
        {/* ---- Right Column: Image ---- */}
        {/* This div centers the image and adds margin on mobile screens */}
        <div className="relative flex justify-center items-center mt-12 lg:mt-0">
          {/* Decorative background blur element */}
          <div className="absolute w-72 h-72 bg-teal-200/50 rounded-full blur-3xl"></div>
          
          {/* The Image itself, with constrained size */}
          <img 
            src={phoneMockup} 
            alt="SortrAid App on a phone" 
            className="w-full max-w-xs md:max-w-sm z-10" 
          />
        </div>

      </div>
    </section>
  );
};

export default Hero;