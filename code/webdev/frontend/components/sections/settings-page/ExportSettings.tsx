"use client";

import React from "react";
import { FileText, ChevronDown, Check } from "lucide-react";

type ExportSettingsProps = {
  autoExportCSV: boolean;
  onAutoExportChange: (val: boolean) => void;
  logRetention: string;
  onLogRetentionChange: (val: string) => void;
};

const RETENTION_OPTIONS = [
  { value: "7", label: "7 Days" },
  { value: "14", label: "14 Days" },
  { value: "30", label: "30 Days" },
  { value: "90", label: "90 Days" },
];

export const ExportSettings = ({
  autoExportCSV,
  onAutoExportChange,
  logRetention,
  onLogRetentionChange,
}: ExportSettingsProps) => {
  return (
    <div className="w-full p-6 bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300/50 flex flex-col gap-6">
      {/* Section Header */}
      <div className="w-full pb-4 border-b border-slate-300/30 flex items-center gap-2">
        <FileText className="size-5 text-sky-700" />
        <h2 className="text-xl font-semibold font-sans text-zinc-900">
          Export &amp; Log Settings
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        {/* Auto-export CSV Toggle */}
        <div className="flex justify-between items-center py-1 gap-4">
          <div className="flex flex-col gap-1">
            <span className="text-sm font-bold font-sans text-zinc-900">
              Auto-export CSV
            </span>
            <span className="text-sm font-normal font-sans text-gray-700">
              Generate shift summaries at end of lot.
            </span>
          </div>

          <button
            type="button"
            role="switch"
            aria-checked={autoExportCSV}
            onClick={() => onAutoExportChange(!autoExportCSV)}
            className={`w-12 h-6 rounded-full p-0.5 transition-colors relative cursor-pointer shrink-0 ${
              autoExportCSV ? "bg-sky-500" : "bg-gray-300"
            }`}
          >
            <div
              className={`size-5 rounded-full bg-white shadow-md transform transition-transform flex items-center justify-center ${
                autoExportCSV ? "translate-x-6 bg-blue-600" : "translate-x-0"
              }`}
            >
              {autoExportCSV && <Check className="size-3 text-white stroke-[3]" />}
            </div>
          </button>
        </div>

        {/* Log Retention Period Dropdown */}
        <div className="flex flex-col gap-2">
          <label className="text-sm font-bold font-sans text-zinc-900">
            Log Retention Period
          </label>
          <div className="relative">
            <select
              value={logRetention}
              onChange={(e) => onLogRetentionChange(e.target.value)}
              className="w-full px-3 py-2.5 bg-white rounded-md outline outline-1 outline-slate-300 appearance-none pr-9 text-base font-normal font-sans text-zinc-900 cursor-pointer focus:outline-sky-500"
            >
              {RETENTION_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 size-5 text-gray-500 pointer-events-none" />
          </div>
        </div>
      </div>
    </div>
  );
};

