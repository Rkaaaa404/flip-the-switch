"use client";

import React from "react";
import { Card } from "../ui/Card";
import { TrendingDown, TrendingUp } from "lucide-react";

type StatCardProps = {
  title: string;
  value: string;
  unit?: string;
  subtext?: string;
  icon: React.ReactNode;
  valueColor?: string;
  delta?: string;
  deltaPositive?: boolean;
};

export const StatCard = ({
  title,
  value,
  unit,
  subtext,
  icon,
  valueColor = "text-zinc-900",
  delta,
  deltaPositive,
}: StatCardProps) => {
  let decorationBg = "bg-sky-500/5"; 
  if (valueColor.includes("green")) decorationBg = "bg-green-500/5";
  if (valueColor.includes("red")) decorationBg = "bg-red-500/5";

  return (
    <Card className="flex-1 flex flex-col gap-3">
      <div className={`size-16 -right-4 -top-4 absolute rounded-bl-[9999px] ${decorationBg}`} />

      <div className="flex flex-row justify-between items-center z-10">
        <span className="text-xs text-gray-700 font-semibold font-sans tracking-wide">{title}</span>
        <span>{icon}</span>
      </div>

      <div className="flex flex-col gap-1 z-10">
        <div className="flex items-baseline gap-2">
          <span className={`text-2xl font-bold font-sans ${valueColor}`}>{value}</span>
          
          {unit && <span className="text-xs text-gray-500 font-normal font-sans">{unit}</span>}
          
          {delta && (
            <span
              className={`text-[11px] font-semibold font-sans flex items-center gap-1 px-1.5 py-0.5 rounded ${
                deltaPositive ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
              }`}
            >
              {delta.startsWith("+") || (!delta.startsWith("-") && parseFloat(delta) >= 0) ? (
                <TrendingUp className="size-3 stroke-[2.5]" />
              ) : (
                <TrendingDown className="size-3 stroke-[2.5]" />
              )}
              {delta}
            </span>
          )}
        </div>
        
        {subtext && <span className="text-xs text-gray-500 font-mono">{subtext}</span>}
      </div>
    </Card>
  );
};
