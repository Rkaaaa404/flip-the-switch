"use client";
import React from "react";
import { motion } from "framer-motion";

type TowerLightProps = {
  signal?: "GREEN" | "YELLOW" | "RED" | "OFF" | string;
};

const signalConfig: Record<string, { label: string; dot: string; glow: string; text: string }> = {
  GREEN: {
    label: "GREEN",
    dot: "bg-green-500",
    glow: "shadow-[0px_0px_10px_0px_rgba(34,197,94,0.70)]",
    text: "text-green-600",
  },
  YELLOW: {
    label: "YELLOW",
    dot: "bg-amber-400",
    glow: "shadow-[0px_0px_10px_0px_rgba(251,191,36,0.70)]",
    text: "text-amber-600",
  },
  RED: {
    label: "RED",
    dot: "bg-red-500",
    glow: "shadow-[0px_0px_10px_0px_rgba(239,68,68,0.70)]",
    text: "text-red-600",
  },
  OFF: {
    label: "OFF",
    dot: "bg-slate-300",
    glow: "shadow-none",
    text: "text-slate-400",
  },
};

export const TowerLight = ({ signal = "GREEN" }: TowerLightProps) => {
  const norm = (signal || "GREEN").toUpperCase();
  const config = signalConfig[norm] || signalConfig.GREEN;

  return (
    <div className="flex items-center gap-2">
      <motion.div
        className={`size-5 rounded-full ${config.dot} ${config.glow}`}
        animate={{
          scale: norm !== "OFF" ? [1, 1.15, 0.95, 1.15, 1] : 1,
          opacity: norm !== "OFF" ? [1, 0.85, 1, 0.85, 1] : 0.6,
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
      <span className={`text-xs font-mono font-bold ${config.text}`}>
        {config.label}
      </span>
    </div>
  );
};
