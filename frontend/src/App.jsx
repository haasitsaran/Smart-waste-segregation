import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Hero from './components/Hero';
import Features from './components/Features';
import Scanner from './components/Scanner';
import ReportIssue from './components/ReportIssue';
import History from './components/History';

// 1. Import the ToastContainer and its CSS
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// A layout component for the main page content
const MainPage = () => (
  <>
    <Hero />
    <Scanner />
    <Features />
  </>
);

function App() {
  return (
    <Router>
      <div className="bg-teal-50 min-h-screen text-gray-800">
        {/* 2. Add the ToastContainer component here */}
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
        <Header />
        <main>
          <Routes>
            {/* Route for the main page */}
            <Route path="/" element={<MainPage />} />
            {/* Route for the report issue page */}
            <Route path="/report-issue" element={<ReportIssue />} />
            {/* Route for the history page */}
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
