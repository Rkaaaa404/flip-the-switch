"use client";

import React from "react";
import { Save, RotateCcw } from "lucide-react";

type BottomSectionProps = {
  onSave: () => void;
  onReset: () => void;
};

export const BottomSection = ({ onSave, onReset }: BottomSectionProps) => {
  return (
    <div className="w-full pt-4 pb-2 border-t border-slate-200 flex justify-end items-center gap-3">
      <button
        type="button"
        onClick={onReset}
        className="px-5 py-2.5 bg-white outline outline-1 outline-slate-300 rounded-md text-zinc-900 text-base font-bold font-sans hover:bg-slate-100 transition-colors cursor-pointer flex items-center gap-2"
      >
        <RotateCcw className="size-4 text-gray-600" />
        <span>Reset to Default</span>
      </button>

      <button
        type="button"
        onClick={onSave}
        className="px-5 py-2.5 bg-sky-500 rounded-md text-white text-base font-bold font-sans hover:bg-sky-600 transition-colors cursor-pointer flex items-center gap-2 shadow-sm"
      >
        <Save className="size-4 text-white" />
        <span>Save Settings</span>
      </button>
    </div>
  );
};

