import React from "react";

type GradeBadgeProps = {
  grade: "A" | "B" | "C";
};

const gradeConfig = {
  A: { bg: "bg-green-100", text: "text-green-600" },
  B: { bg: "bg-amber-100", text: "text-amber-600" },
  C: { bg: "bg-red-100",   text: "text-red-600"   },
};

export const GradeBadge = ({ grade }: GradeBadgeProps) => {
  const { bg, text } = gradeConfig[grade];
  return (
    <div className={`w-6 py-1 rounded-full inline-flex justify-center items-center ${bg}`}>
      <span className={`text-xs font-bold font-sans ${text}`}>{grade}</span>
    </div>
  );
};
