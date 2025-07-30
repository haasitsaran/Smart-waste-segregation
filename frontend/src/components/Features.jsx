// import React from 'react';
// import FeatureCard from './FeatureCard';
// // Import the necessary icons
// import { FiMessageSquare, FiMapPin, FiCpu } from 'react-icons/fi'; // Changed FiClock to FiCpu

// const iconClass = "w-6 h-6 text-green-600";

// // Updated data array with the new "Craft Videos" card
// const featuresData = [
//   { 
//     icon: <FiCpu className={iconClass} />, 
//     title: "Craft Videos", 
//     description: "Get creative video tutorials to turn waste into wonderful crafts and useful items.", 
//     linkText: "Browse Videos",
//     to: "/craft-videos" // Route for the new Craft Videos page
//   },
//   { 
//     icon: <FiMessageSquare className={iconClass} />, 
//     title: "Report Issue", 
//     description: "Help clean your community by reporting litter spots with GPS location.", 
//     linkText: "Report", 
//     to: "/report-issue" // Route for the Report Issue page
//   },
//   { 
//     icon: <FiMapPin className={iconClass} />, 
//     title: "Find Centers", 
//     description: "Locate nearby recycling centers and get directions to proper disposal facilities.", 
//     linkText: "Find Nearby" // This one won't be a link for now
//   },
// ];

// const Features = () => {
//   return (
//     <section className="bg-gray-50/70 py-16 md:py-24">
//       <div className="container mx-auto px-6">
//         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
//           {featuresData.map((feature, index) => <FeatureCard key={index} {...feature} />)}
//         </div>
//       </div>
//     </section>
//   );
// };

// export default Features;

import React from 'react';
import FeatureCard from './FeatureCard';
import { FiMessageSquare, FiMapPin, FiCpu } from 'react-icons/fi';

const iconClass = "w-6 h-6 text-green-600";

const featuresData = [
  { 
    icon: <FiCpu className={iconClass} />, 
    title: "Craft Videos", 
    description: "Get creative video tutorials to turn waste into wonderful crafts.", 
    linkText: "Browse Videos",
    to: "/craft-videos"
  },
  { 
    icon: <FiMessageSquare className={iconClass} />, 
    title: "Report Issue", 
    description: "Help clean your community by reporting litter spots with GPS.", 
    linkText: "Report", 
    to: "/report-issue"
  },
  { 
    icon: <FiMapPin className={iconClass} />, 
    title: "Find Centers", 
    description: "Locate nearby recycling centers based on your recent scans.", 
    linkText: "Find Nearby",
    to: "/find-nearby" // Add the route link here
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
