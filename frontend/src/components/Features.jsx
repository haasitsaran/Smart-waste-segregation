import React from 'react';
import FeatureCard from './FeatureCard';
// Import the necessary icons
import { FiMessageSquare, FiMapPin, FiClock } from 'react-icons/fi';

const iconClass = "w-6 h-6 text-green-600";

// Updated data array with 'to' properties for routing
const featuresData = [
  { 
    icon: <FiClock className={iconClass} />, 
    title: "Detection History", 
    description: "View your past waste detections and stats.", 
    linkText: "View History",
    to: "/history" // Route for the History page
  },
  { 
    icon: <FiMessageSquare className={iconClass} />, 
    title: "Report Issue", 
    description: "Help clean your community by reporting litter spots with GPS location.", 
    linkText: "Report", 
    to: "/report-issue" // Route for the Report Issue page
  },
  { 
    icon: <FiMapPin className={iconClass} />, 
    title: "Find Centers", 
    description: "Locate nearby recycling centers and get directions to proper disposal facilities.", 
    linkText: "Find Nearby" // This one won't be a link for now
  },
];

const Features = () => {
  return (
    <section className="bg-gray-50/70 py-16 md:py-24">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuresData.map((feature, index) => <FeatureCard key={index} {...feature} />)}
        </div>
      </div>
    </section>
  );
};

export default Features;
