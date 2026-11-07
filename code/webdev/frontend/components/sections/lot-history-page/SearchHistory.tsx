"use client";

import React from "react";
import { Search, ChevronDown, Download, RotateCcw } from "lucide-react";

const FISH_TYPES = [
  { value: "all", label: "Semua Jenis Ikan" },
  { value: "Tuna", label: "Tuna" },
  { value: "Mackarel", label: "Mackarel" },
  { value: "Nila", label: "Nila" },
];

const FAMILIES = FISH_TYPES;

const GRADES = [
  { value: "all", label: "Semua Grade Mutu" },
  { value: "A", label: "Grade A (Prima / Ekspor)" },
  { value: "B", label: "Grade B (Segar / Domestik)" },
  { value: "C", label: "Grade C (Reject / Busuk)" },
];

const DECISIONS = [
  { value: "all", label: "Semua Keputusan" },
  { value: "PASS", label: "PASS (Lolos Mutu)" },
  { value: "CONDITIONAL", label: "CONDITIONAL (Verifikasi)" },
  { value: "FAIL", label: "FAIL (Reject)" },
];

type SearchHistoryProps = {
  search: string;
  onSearchChange: (val: string) => void;
  family: string;
  onFamilyChange: (val: string) => void;
  grade: string;
  onGradeChange: (val: string) => void;
  decision: string;
  onDecisionChange: (val: string) => void;
  dateFrom: string;
  onDateFromChange: (val: string) => void;
  dateTo: string;
  onDateToChange: (val: string) => void;
  onClearFilters: () => void;
};

export const SearchHistory = ({
  search,
  onSearchChange,
  family,
  onFamilyChange,
  grade,
  onGradeChange,
  decision,
  onDecisionChange,
  dateFrom,
  onDateFromChange,
  dateTo,
  onDateToChange,
  onClearFilters,
}: SearchHistoryProps) => {
  const handleExportCsv = () => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    window.open(`${baseUrl}/lots/export?format=csv`, "_blank");
  };

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Search & Filter Card */}
      <div className="w-full bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 p-5 flex flex-col gap-4">
        {/* Row 1: Search Input & Dropdowns */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 w-full">
          {/* Search Input */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
            <input
              type="text"
              value={search}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Cari Lot ID (LOT-2026)..."
              className="w-full pl-9 pr-4 py-2 bg-slate-50 rounded-sm outline outline-1 outline-slate-300 text-sm font-sans text-zinc-900 placeholder:text-gray-400 focus:outline-sky-500"
            />
          </div>

          {/* Fish Type Filter */}
          <div className="relative">
            <select
              value={family}
              onChange={(e) => onFamilyChange(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 rounded-sm outline outline-1 outline-slate-300 appearance-none pr-9 text-sm font-sans text-zinc-900 cursor-pointer focus:outline-sky-500"
            >
              {FISH_TYPES.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
          </div>

          {/* Grade Filter */}
          <div className="relative">
            <select
              value={grade}
              onChange={(e) => onGradeChange(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 rounded-sm outline outline-1 outline-slate-300 appearance-none pr-9 text-sm font-sans text-zinc-900 cursor-pointer focus:outline-sky-500"
            >
              {GRADES.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
          </div>

          {/* Decision Filter */}
          <div className="relative">
            <select
              value={decision}
              onChange={(e) => onDecisionChange(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 rounded-sm outline outline-1 outline-slate-300 appearance-none pr-9 text-sm font-sans text-zinc-900 cursor-pointer focus:outline-sky-500"
            >
              {DECISIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
          </div>
        </div>

        {/* Row 2: Date Range & Actions */}
        <div className="flex flex-wrap items-center justify-between gap-3 w-full pt-1 border-t border-slate-100">
          {/* Date Range Picker */}
          <div className="flex items-center gap-2 bg-slate-50 rounded-sm outline outline-1 outline-slate-300 px-3 py-1.5 text-xs font-sans">
            <span className="text-gray-600 font-medium">Dari:</span>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => onDateFromChange(e.target.value)}
              className="bg-transparent border-none text-xs font-mono text-zinc-900 focus:outline-none cursor-pointer"
            />
            <span className="text-gray-600 font-medium ml-2">Sampai:</span>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => onDateToChange(e.target.value)}
              className="bg-transparent border-none text-xs font-mono text-zinc-900 focus:outline-none cursor-pointer"
            />
          </div>

          {/* Right Action Buttons */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onClearFilters}
              className="text-xs font-semibold font-sans text-sky-700 hover:text-sky-900 transition-colors flex items-center gap-1 cursor-pointer"
            >
              <RotateCcw className="size-3" />
              <span>Reset Filter</span>
            </button>

            <button
              type="button"
              onClick={handleExportCsv}
              className="flex items-center gap-1.5 px-3.5 py-1.5 bg-sky-50 outline outline-1 outline-sky-700 rounded-sm text-sky-700 text-xs font-bold font-sans hover:bg-sky-100 transition-colors cursor-pointer shadow-xs"
            >
              <Download className="size-3.5 text-sky-700" />
              <span>Ekspor CSV</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
