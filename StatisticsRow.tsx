import React from "react";
import StatCard from "./StatCard";

interface StatisticsRowProps {
  data: {
    title: string;
    value: number | string;
    comparison: string;
    color: "green" | "yellow" | "red";
    // icon: React.ReactNode;
  }[];
}

const StatisticsRow: React.FC<StatisticsRowProps> = ({ data }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {data.map((stat, index) => (
        <StatCard
          key={index}
          title={stat.title}
          value={stat.value}
          comparison={stat.comparison}
          color={stat.color}
          // icon={stat.icon}
        />
      ))}
    </div>
  );
};

export default StatisticsRow;
