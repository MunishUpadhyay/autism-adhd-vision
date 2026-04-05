import React from 'react';

const ScoreCard = ({ title, value, color, Icon, delayClass = "" }) => {
  // Guarantee values parse between absolute 0 and 1 before converting to normalized GUI percentages securely.
  const numericValue = typeof value === 'number' && !isNaN(value) ? value : 0;
  const percentage = Math.min(Math.max(numericValue * 100, 0), 100).toFixed(0);
  
  return (
    <div className={`bg-white rounded-2xl shadow-md p-6 flex flex-col items-start gap-2 ${delayClass} animate-fade-in opacity-0`}>
      <div className="flex items-center gap-2 mb-1">
        {Icon && <Icon className="w-4 h-4 text-slate-400" />}
        <h3 className="text-slate-500 font-semibold text-sm uppercase tracking-wide">{title}</h3>
      </div>
      
      <div className="w-full flex items-center justify-between">
        <span className="text-3xl font-black text-slate-800">{percentage}%</span>
      </div>
      
      <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden mt-3 shadow-inner">
        <div 
          className={`h-full rounded-full transition-all duration-1000 ease-out ${color || 'bg-blue-500'}`} 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ScoreCard;
