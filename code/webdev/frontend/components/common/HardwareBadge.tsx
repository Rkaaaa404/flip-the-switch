import React from "react";

type HardwareBadgeProps = {
  status?: string;
};

export const HardwareBadge = ({ status = "Online" }: HardwareBadgeProps) => {
  const norm = (status || "").toLowerCase();

  const isPositive = norm === "online" || norm === "active" || norm === "running";
  const isWarning = norm === "warning" || norm === "slow";

  const config = isPositive
    ? { bg: "bg-green-100 border-green-200", dot: "bg-green-600", text: "text-green-700", label: status.toUpperCase() }
    : isWarning
    ? { bg: "bg-amber-100 border-amber-200", dot: "bg-amber-500", text: "text-amber-700", label: status.toUpperCase() }
    : { bg: "bg-red-100 border-red-200", dot: "bg-red-500", text: "text-red-700", label: status.toUpperCase() };

  return (
    <div className={`px-2.5 py-0.5 rounded-full inline-flex items-center gap-1.5 border ${config.bg}`}>
      <div className={`size-1.5 rounded-full ${config.dot}`} />
      <span className={`text-xs font-bold font-mono ${config.text}`}>{config.label}</span>
    </div>
  );
};
