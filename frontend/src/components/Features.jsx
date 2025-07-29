import React from 'react';
import FeatureCard from './FeatureCard';
import { FiCamera, FiCpu, FiMessageSquare, FiZap, FiAward, FiMapPin } from 'react-icons/fi';

const iconClass = "w-6 h-6 text-green-600";
const featuresData = [
  { icon: <FiCamera className={iconClass} />, title: "Live Detection", description: "Real-time AI identifies waste types with 95% accuracy using your phone camera.", linkText: "Try Scanner" },
  { icon: <FiCpu className={iconClass} />, title: "Upcycle Ideas", description: "Get creative video tutorials to turn waste into wonderful crafts and useful items.", linkText: "Browse Videos" },
  { icon: <FiMessageSquare className={iconClass} />, title: "Report Litter", description: "Help clean your community by reporting litter spots with GPS location.", linkText: "Make Report" },
  { icon: <FiZap className={iconClass} />, title: "Eco Tips", description: "Daily environmental facts and tips to reduce waste and live more sustainably.", linkText: "Learn More" },
  { icon: <FiAward className={iconClass} />, title: "Earn Rewards", description: "Collect points, unlock badges, and compete with friends on leaderboards.", linkText: "View Progress" },
  { icon: <FiMapPin className={iconClass} />, title: "Find Centers", description: "Locate nearby recycling centers and get directions to proper disposal facilities.", linkText: "Find Nearby" },
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