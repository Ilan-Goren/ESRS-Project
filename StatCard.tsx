import React from 'react';

interface StatCardProps {
  // icon: React.ReactNode;        // The icon for the metric
  title: string;                // Title of the stat (e.g., "Total Users")
  value: string | number;       // The value of the metric
  comparison: string;           // Comparison text (e.g., "↑ 15% from last month")
  color: 'green' | 'yellow' | 'red';  // The color for the status (e.g., "good", "warning", "critical")
}

const StatCard: React.FC<StatCardProps> = ({ /*icon,*/ title, value, comparison, color }) => {
  const getColorClass = () => {
    switch (color) {
      case 'green':
        return 'bg-green-100 text-green-700';
      case 'yellow':
        return 'bg-yellow-100 text-yellow-700';
      case 'red':
        return 'bg-red-100 text-red-700';
      default:
        return '';
    }
  };

  return (
    <div className={`flex items-center p-4 rounded-lg shadow-lg ${getColorClass()} max-w-xs`}>
      <div className="mr-4">
        
      </div>
      <div>
        <h3 className="text-lg font-semibold">{title}</h3>
        <p className="text-2xl font-bold">{value}</p>
        <p className="text-sm">{comparison}</p>
      </div>
    </div>
  );
};

export default StatCard;
