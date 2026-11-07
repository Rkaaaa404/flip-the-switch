"use client";

import React from "react";
import Link from "next/link";
import { X, ExternalLink, Trash2, ShieldCheck, Clock, Layers } from "lucide-react";
import { StorageSlot } from "@/types";

interface SlotDetailDrawerProps {
  slot: StorageSlot | null;
  onClose: () => void;
  onClearSlot: (slotId: string) => Promise<void>;
  isClearing?: boolean;
}

function calculateDuration(storedAtStr?: string | null): string {
  if (!storedAtStr) return "Just now";
  try {
    const storedDate = new Date(storedAtStr);
    const now = new Date();
    const diffMs = Math.max(0, now.getTime() - storedDate.getTime());
    const totalMins = Math.floor(diffMs / (1000 * 60));
    const hours = Math.floor(totalMins / 60);
    const mins = totalMins % 60;

    if (hours > 0) {
      return `${hours} hour${hours > 1 ? "s" : ""} ${mins} minute${mins !== 1 ? "s" : ""}`;
    }
    return `${mins} minute${mins !== 1 ? "s" : ""}`;
  } catch {
    return "N/A";
  }
}

export const SlotDetailDrawer = ({
  slot,
  onClose,
  onClearSlot,
  isClearing = false,
}: SlotDetailDrawerProps) => {
  if (!slot) return null;

  const lot = slot.lot;
  const lotId = slot.lotId || slot.lot_id || lot?.lotId || lot?.lot_id || "N/A";
  const fishFamily = lot?.fishFamily || lot?.fish_family || lot?.family || "Tuna";
  const grade = lot?.grade || "A";
  const conf = lot
    ? Math.round(
        lot.confidence !== undefined
          ? lot.confidence > 1.0 ? lot.confidence : lot.confidence * 100
          : (lot.grade_confidence ? lot.grade_confidence * 100 : 92.1)
      )
    : 92;
  const defectsCount = lot?.defectsCount ?? lot?.defects_count ?? 0;
  const storedSince = slot.assignedAt || slot.assigned_at || lot?.stored_at || "2026-08-22 10:30:00";
  const duration = calculateDuration(storedSince);

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-slate-900/40 backdrop-blur-xs transition-opacity animate-in fade-in duration-200">
      {/* Click outside backdrop to close */}
      <div className="flex-1 cursor-pointer" onClick={onClose} />

      {/* Drawer Container */}
      <div className="w-full max-w-sm h-full bg-white shadow-2xl flex flex-col justify-between border-l border-slate-200 animate-in slide-in-from-right duration-250">
        {/* Header */}
        <div className="p-6 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-xl font-bold font-sans text-zinc-900">
            Slot {slot.slotId || slot.slot_id}
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-sm text-gray-400 hover:text-zinc-900 hover:bg-slate-100 transition-colors cursor-pointer"
          >
            <X className="size-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 flex-1 overflow-y-auto flex flex-col gap-6">
          {/* Zone Pill */}
          <div>
            <span
              className={`inline-block px-3 py-1 rounded-full text-xs font-bold font-sans tracking-wide uppercase ${
                slot.zone === "cold"
                  ? "bg-sky-50 text-sky-700 border border-sky-200"
                  : "bg-indigo-50 text-indigo-700 border border-indigo-200"
              }`}
            >
              {slot.zone === "cold" ? "Cold Zone (0–4°C)" : "Frozen Zone (≤ -18°C)"}
            </span>
          </div>

          {/* Details List */}
          <div className="flex flex-col gap-4 text-sm font-sans">
            {/* Lot ID */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                LOT ID
              </span>
              <span className="text-lg font-bold font-mono text-sky-600 tracking-tight mt-0.5">
                {lotId}
              </span>
            </div>

            {/* Fish Type */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                JENIS IKAN
              </span>
              <span className="text-base font-semibold text-zinc-800 mt-0.5">
                {fishFamily}
              </span>
            </div>

            {/* Grade */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                GRADE
              </span>
              <div className="mt-1">
                <span
                  className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-sm text-xs font-bold font-sans ${
                    grade === "A"
                      ? "bg-green-100 text-green-800 border border-green-300"
                      : "bg-amber-100 text-amber-800 border border-amber-300"
                  }`}
                >
                  <span className="size-1.5 rounded-full bg-current" />
                  GRADE {grade}
                </span>
              </div>
            </div>

            {/* Confidence */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                CONFIDENCE
              </span>
              <span className="text-base font-bold font-mono text-zinc-900 mt-0.5">
                {conf}%
              </span>
            </div>

            {/* Defects */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                DEFECTS
              </span>
              <span className="text-base font-semibold text-zinc-800 mt-0.5">
                {defectsCount}
              </span>
            </div>

            {/* Stored Since */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                STORED SINCE
              </span>
              <span className="text-sm font-mono text-zinc-700 mt-0.5">
                {storedSince}
              </span>
            </div>

            {/* Duration */}
            <div className="flex flex-col">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                DURATION
              </span>
              <span className="text-sm font-medium text-zinc-800 mt-0.5">
                {duration}
              </span>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-6 border-t border-slate-200 flex flex-col gap-3 bg-slate-50/50">
          <Link
            href={`/history/${lotId}`}
            className="w-full py-2.5 px-4 rounded-sm border border-sky-600 bg-white text-sky-700 font-bold text-sm font-sans hover:bg-sky-50 transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-xs"
          >
            <ExternalLink className="size-4" />
            <span>View Inspection Detail</span>
          </Link>

          <button
            type="button"
            onClick={() => onClearSlot(slot.slotId || slot.slot_id)}
            disabled={isClearing}
            className="w-full py-2.5 px-4 rounded-sm border border-rose-300 bg-white text-rose-700 font-bold text-sm font-sans hover:bg-rose-50 transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-xs disabled:opacity-50"
          >
            <Trash2 className="size-4" />
            <span>{isClearing ? "Clearing..." : "Clear Slot"}</span>
          </button>

          <p className="text-[11px] font-sans text-gray-400 text-center mt-1">
            Clearing a slot does not delete the inspection record.
          </p>
        </div>
      </div>
    </div>
  );
};
