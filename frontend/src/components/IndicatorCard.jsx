import React from 'react';

const IndicatorCard = ({ title, status }) => {
  const getStatusColor = () => {
    switch(status?.toLowerCase()) {
      case 'low': return 'text-green-500';
      case 'stable': return 'text-green-500';
      
      case 'medium': return 'text-yellow-500';
      case 'repetitive': return 'text-yellow-500';
      case 'uncertain': return 'text-yellow-600'; // explicitly shifting uncertain from dull gray to soft amber context
      
      case 'high': return 'text-red-500';
      case 'erratic': return 'text-red-500';
      
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col items-center justify-center text-center">
      <h3 className="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wide">{title}</h3>
      <span className={`text-2xl font-bold capitalize ${getStatusColor()}`}>
        {status}
      </span>
    </div>
  );
};

export default IndicatorCard;
