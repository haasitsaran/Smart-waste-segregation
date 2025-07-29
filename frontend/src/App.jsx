import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Features from './components/Features';
import Scanner from './components/Scanner';

function App() {
  return (
    // Set a background color for the entire page
    <div className="bg-teal-50 min-h-screen text-gray-800">
      <Header />
      <main>
        <Hero />
        <Scanner />
        <Features />
      </main>
    </div>
  );
}

export default App;