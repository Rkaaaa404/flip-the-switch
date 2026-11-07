import React from "react";
import { Decision } from "@/types";

type StatusBadgeProps = {
  decision: Decision | string;
};

export const StatusBadge = ({ decision }: StatusBadgeProps) => {
  const normalized = (decision || "PASS").toUpperCase();

  if (normalized === "PASS") {
    return (
      <div className="px-2.5 py-1 rounded-full inline-flex items-center gap-1 bg-green-100 border border-green-200">
        <span className="text-xs font-bold font-sans text-green-700">✓ PASS</span>
      </div>
    );
  }

  if (normalized === "CONDITIONAL") {
    return (
      <div className="px-2.5 py-1 rounded-full inline-flex items-center gap-1 bg-amber-100 border border-amber-200">
        <span className="text-xs font-bold font-sans text-amber-700">⚠ CONDITIONAL</span>
      </div>
    );
  }

  return (
    <div className="px-2.5 py-1 rounded-full inline-flex items-center gap-1 bg-red-100 border border-red-200">
      <span className="text-xs font-bold font-sans text-red-700">✗ FAIL</span>
    </div>
  );
};
