import React, { useState } from 'react';
import VideoInput from '../components/VideoInput';
import Dashboard from '../components/Dashboard';

const Home = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resetKey, setResetKey] = useState(0);

  const handleAnalysisStart = () => {
    setData(null);
    setError(null);
    setLoading(true);
  };

  const handleAnalysisComplete = (result) => {
    setData(result);
    setLoading(false);
  };

  const handleAnalysisError = (errMsg) => {
    setError(errMsg || "Analysis failed. Please try another video or check format.");
    setLoading(false);
  };

  // Robust universal layout wiping hook to reset all child environments natively
  const handleResetUI = () => {
    setData(null);
    setError(null);
    setLoading(false);
    setResetKey(prev => prev + 1); // Instantly shreds the localized VideoInput state
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans antialiased text-slate-900 selection:bg-indigo-100 flex flex-col items-center pt-8 pb-20">
      <div className="w-full max-w-6xl px-6 space-y-6">
        
        {/* Header Section with built-in localized Reset Tracking hook */}
        <header className="flex flex-col md:flex-row items-center justify-between mb-8 pb-6 border-b border-slate-200">
          <div className="text-center md:text-left mb-4 md:mb-0">
            <h1 className="text-3xl font-bold text-slate-800 tracking-tight">Behavioral Vision Board</h1>
            <p className="text-slate-500 font-medium tracking-wide mt-1">Upload clinical footage to extract spatial motion data natively</p>
          </div>
          
          {/* Conditional Top-Level Reset Action */}
          <div className="transition-opacity duration-500">
            {(data !== null || error !== null || loading) && (
              <button 
                onClick={handleResetUI}
                className="flex items-center gap-2 px-5 py-2 rounded-full border border-slate-300 text-sm font-bold text-slate-600 hover:bg-slate-200 hover:text-slate-800 transition-all shadow-sm bg-white"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                New Analysis
              </button>
            )}
          </div>
        </header>

        {/* Upload Section securely bound to the React Re-Mount identity */}
        <VideoInput 
          key={resetKey}
          onAnalysisStart={handleAnalysisStart}
          onAnalysisComplete={handleAnalysisComplete}
          onAnalysisError={handleAnalysisError}
        />

        {/* Loading & Error States */}
        {loading && (
          <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-md p-6 border border-indigo-100 text-center animate-pulse">
            <span className="font-semibold text-indigo-600 tracking-wide">Analyzing visual patterns using computer vision pipeline...</span>
          </div>
        )}
        
        {error && !loading && (
          <div className="max-w-4xl mx-auto bg-slate-100 rounded-2xl shadow-sm p-6 border border-slate-200 text-center">
            <span className="font-medium text-slate-600">Analysis failed. Please try another video or check format.</span>
          </div>
        )}

        {/* Results Dashboard completely decoupled gracefully appearing underneath */}
        {data && !loading && !error && (
          <div className="transition-all duration-700 ease-in-out">
             <Dashboard data={data} />
          </div>
        )}

      </div>
    </div>
  );
};

export default Home;
