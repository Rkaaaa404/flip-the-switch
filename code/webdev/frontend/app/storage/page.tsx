"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  Boxes,
  Snowflake,
  Clock,
  Info,
  X,
  Loader2,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
} from "lucide-react";
import {
  fetchStorageSlots,
  fetchPendingStorageLots,
  assignStorageSlot,
  clearStorageSlot,
} from "@/lib/api";
import { StorageOverview, StorageSlot, LotRecord } from "@/types";
import { SlotDetailDrawer } from "@/components/sections/storage-page/SlotDetailDrawer";

export default function StoragePage() {
  const [overview, setOverview] = useState<StorageOverview | null>(null);
  const [pendingLots, setPendingLots] = useState<LotRecord[]>([]);
  const [selectedZone, setSelectedZone] = useState<"all" | "cold" | "frozen">("all");
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Interactive Placing Mode State
  const [placingLot, setPlacingLot] = useState<LotRecord | null>(null);
  const [suggestedZone, setSuggestedZone] = useState<"cold" | "frozen">("cold");
  const [isAssigning, setIsAssigning] = useState<boolean>(false);
  const [notification, setNotification] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Selected Slot for Drawer View
  const [activeSlot, setActiveSlot] = useState<StorageSlot | null>(null);
  const [isClearing, setIsClearing] = useState<boolean>(false);

  const loadData = useCallback(async () => {
    try {
      const [slotsData, pendingData] = await Promise.all([
        fetchStorageSlots(),
        fetchPendingStorageLots(),
      ]);
      setOverview(slotsData);
      setPendingLots(pendingData);
    } catch (err) {
      console.warn("Failed to load storage data:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleStartPlacing = (lot: LotRecord, zone: "cold" | "frozen") => {
    setPlacingLot(lot);
    setSuggestedZone(zone);
    setSelectedZone(zone === "cold" ? "cold" : "frozen");
  };

  const handleCancelPlacing = () => {
    setPlacingLot(null);
  };

  const handleSlotClick = async (slot: StorageSlot) => {
    // If placing mode is active and this slot is empty
    if (placingLot && !slot.lot_id) {
      setIsAssigning(true);
      try {
        const lotIdToAssign = placingLot.lotId || placingLot.lot_id || `LOT-${placingLot.id}`;
        await assignStorageSlot(slot.slot_id, lotIdToAssign);
        setNotification({
          type: "success",
          text: `Lot ${lotIdToAssign} berhasil ditempatkan ke Slot ${slot.slot_id}!`,
        });
        setPlacingLot(null);
        await loadData();
      } catch (err: any) {
        setNotification({
          type: "error",
          text: err?.message || "Gagal menempatkan lot ke slot.",
        });
      } finally {
        setIsAssigning(false);
        setTimeout(() => setNotification(null), 4000);
      }
      return;
    }

    // If slot is occupied, open detail drawer
    if (slot.lot_id) {
      setActiveSlot(slot);
    }
  };

  const handleClearSlot = async (slotId: string) => {
    setIsClearing(true);
    try {
      await clearStorageSlot(slotId);
      setActiveSlot(null);
      setNotification({
        type: "success",
        text: `Slot ${slotId} berhasil dikosongkan!`,
      });
      await loadData();
    } catch (err: any) {
      setNotification({
        type: "error",
        text: err?.message || "Gagal mengosongkan slot.",
      });
    } finally {
      setIsClearing(false);
      setTimeout(() => setNotification(null), 4000);
    }
  };

  const slots = overview?.slots || [];
  const coldSlots = slots.filter((s) => s.zone === "cold");
  const frozenSlots = slots.filter((s) => s.zone === "frozen");

  const coldOccupied = coldSlots.filter((s) => s.lot_id).length;
  const coldAvailable = coldSlots.length - coldOccupied;

  const frozenOccupied = frozenSlots.filter((s) => s.lot_id).length;
  const frozenAvailable = frozenSlots.length - frozenOccupied;

  const totalSlots = overview?.total_slots || 35;
  const totalOccupied = overview?.occupied || 0;
  const totalAvailable = overview?.available || 35;
  const pendingCount = pendingLots.length;

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      {/* Notification Toast */}
      {notification && (
        <div
          className={`p-3.5 rounded-md border flex items-center gap-2 text-sm font-sans animate-in fade-in duration-200 ${
            notification.type === "success"
              ? "bg-emerald-50 text-emerald-800 border-emerald-300"
              : "bg-rose-50 text-rose-800 border-rose-300"
          }`}
        >
          {notification.type === "success" ? (
            <CheckCircle2 className="size-4 text-emerald-600 shrink-0" />
          ) : (
            <AlertCircle className="size-4 text-rose-600 shrink-0" />
          )}
          <span>{notification.text}</span>
        </div>
      )}

      {/* Top Stat KPI Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5 w-full">
        <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500 font-sans">Total Slots</span>
          <span className="text-2xl font-black text-slate-900 font-sans mt-1">{totalSlots}</span>
        </div>
        <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500 font-sans">Occupied</span>
          <span className="text-2xl font-black text-sky-600 font-sans mt-1">{totalOccupied}</span>
        </div>
        <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500 font-sans">Available</span>
          <span className="text-2xl font-black text-emerald-600 font-sans mt-1">{totalAvailable}</span>
        </div>
        <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col justify-between">
          <span className="text-xs font-semibold text-slate-500 font-sans">Pending Assignment</span>
          <span className="text-2xl font-black text-amber-600 font-sans mt-1">{pendingCount}</span>
        </div>
      </div>

      {/* Zone Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3 px-4 rounded-lg border border-slate-200 shadow-xs">
        <span className="text-xs font-bold text-slate-700 font-sans">
          Filter Tampilan Zona:
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setSelectedZone("all")}
            className={`px-3 py-1 text-xs font-bold font-sans rounded-sm transition-colors cursor-pointer ${
              selectedZone === "all"
                ? "bg-sky-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            Semua Zona
          </button>
          <button
            type="button"
            onClick={() => setSelectedZone("cold")}
            className={`px-3 py-1 text-xs font-bold font-sans rounded-sm transition-colors cursor-pointer ${
              selectedZone === "cold"
                ? "bg-sky-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            Cold Zone (0–4°C)
          </button>
          <button
            type="button"
            onClick={() => setSelectedZone("frozen")}
            className={`px-3 py-1 text-xs font-bold font-sans rounded-sm transition-colors cursor-pointer ${
              selectedZone === "frozen"
                ? "bg-indigo-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            Frozen Zone (≤ -18°C)
          </button>
        </div>
      </div>

      {/* Interactive Placing Alert Banner */}
      {placingLot && (
        <div className="w-full bg-sky-500 text-white rounded-lg px-4 py-3 flex items-center justify-between shadow-md animate-in slide-in-from-top-2 duration-200">
          <div className="flex items-center gap-2 text-sm font-sans font-medium">
            <Info className="size-5 shrink-0" />
            <span>
              Placing: <strong className="font-mono">{placingLot.lotId || placingLot.lot_id}</strong> ({placingLot.fishFamily || placingLot.fish_family || "Tuna"}, Grade {placingLot.grade || "A"}) — Klik slot hijau yang kosong untuk menempatkan lot.
            </span>
          </div>
          <button
            type="button"
            onClick={handleCancelPlacing}
            className="p-1 rounded-full hover:bg-sky-600 transition-colors text-white cursor-pointer"
          >
            <X className="size-5" />
          </button>
        </div>
      )}

      {/* Main Grid & Side Panel Layout */}
      <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN: Storage Map Grids (col-span-8) */}
        <div className="lg:col-span-8 flex flex-col gap-6">

          {/* 1. Cold Zone Card */}
          {(selectedZone === "all" || selectedZone === "cold") && (
            <div className="w-full bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <Snowflake className="size-5 text-sky-600" />
                  <h3 className="text-base font-bold font-sans text-zinc-900">
                    Cold Zone
                  </h3>
                </div>
                <span className="text-xs font-sans font-semibold text-gray-600 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
                  {coldAvailable} available • {coldOccupied} occupied
                </span>
              </div>

              {/* 5x5 Grid */}
              <div className="grid grid-cols-5 gap-3">
                {coldSlots.map((slot) => {
                  const isOccupied = Boolean(slot.lot_id);
                  const isHighlightPlacing = placingLot && !isOccupied && suggestedZone === "cold";

                  return (
                    <div
                      key={slot.slot_id}
                      onClick={() => handleSlotClick(slot)}
                      className={`min-h-[84px] rounded-lg p-2 flex flex-col justify-between transition-all cursor-pointer select-none ${
                        isOccupied
                          ? "bg-sky-50 border border-sky-300 hover:border-sky-500 hover:shadow-xs"
                          : isHighlightPlacing
                          ? "bg-emerald-50 border-2 border-dashed border-emerald-500 hover:bg-emerald-100 animate-pulse"
                          : "bg-white border-2 border-dashed border-slate-300 hover:border-slate-400"
                      }`}
                    >
                      <div className="flex justify-between items-start">
                        <span className={`text-[11px] font-mono font-bold ${isOccupied ? "text-gray-500" : "text-gray-400"}`}>
                          {slot.slot_id}
                        </span>
                        {isOccupied && slot.lot && (
                          <span className="size-4 rounded-full bg-emerald-600 text-white font-bold text-[9px] flex items-center justify-center">
                            {slot.lot.grade || "A"}
                          </span>
                        )}
                      </div>

                      {isOccupied ? (
                        <div className="flex flex-col mt-0.5">
                          <span className="text-[10px] font-mono font-bold text-sky-700 truncate leading-tight">
                            {slot.lot_id}
                          </span>
                          <span className="text-[9px] font-sans text-gray-500 truncate">
                            {slot.lot?.fishFamily || slot.lot?.fish_family || "Scombridae"}
                          </span>
                        </div>
                      ) : (
                        <div className="flex items-center justify-center flex-1">
                          <span className={`text-xs font-mono font-semibold ${isHighlightPlacing ? "text-emerald-700" : "text-gray-300"}`}>
                            {isHighlightPlacing ? "Place Here" : slot.slot_id}
                          </span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* 2. Frozen Zone Card */}
          {(selectedZone === "all" || selectedZone === "frozen") && (
            <div className="w-full bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-6 flex flex-col gap-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <Snowflake className="size-5 text-indigo-600" />
                  <h3 className="text-base font-bold font-sans text-zinc-900">
                    Frozen Zone
                  </h3>
                </div>
                <span className="text-xs font-sans font-semibold text-gray-600 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
                  {frozenAvailable} available • {frozenOccupied} occupied
                </span>
              </div>

              {/* 2x5 Grid */}
              <div className="grid grid-cols-5 gap-3">
                {frozenSlots.map((slot) => {
                  const isOccupied = Boolean(slot.lot_id);
                  const isHighlightPlacing = placingLot && !isOccupied && suggestedZone === "frozen";

                  return (
                    <div
                      key={slot.slot_id}
                      onClick={() => handleSlotClick(slot)}
                      className={`min-h-[84px] rounded-lg p-2 flex flex-col justify-between transition-all cursor-pointer select-none ${
                        isOccupied
                          ? "bg-indigo-50 border border-indigo-300 hover:border-indigo-500 hover:shadow-xs"
                          : isHighlightPlacing
                          ? "bg-emerald-50 border-2 border-dashed border-emerald-500 hover:bg-emerald-100 animate-pulse"
                          : "bg-white border-2 border-dashed border-slate-300 hover:border-slate-400"
                      }`}
                    >
                      <div className="flex justify-between items-start">
                        <span className={`text-[11px] font-mono font-bold ${isOccupied ? "text-gray-500" : "text-gray-400"}`}>
                          {slot.slot_id}
                        </span>
                        {isOccupied && slot.lot && (
                          <span className="size-4 rounded-full bg-indigo-600 text-white font-bold text-[9px] flex items-center justify-center">
                            {slot.lot.grade || "A"}
                          </span>
                        )}
                      </div>

                      {isOccupied ? (
                        <div className="flex flex-col mt-0.5">
                          <span className="text-[10px] font-mono font-bold text-indigo-700 truncate leading-tight">
                            {slot.lot_id}
                          </span>
                          <span className="text-[9px] font-sans text-gray-500 truncate">
                            {slot.lot?.fishFamily || slot.lot?.fish_family || "Scombridae"}
                          </span>
                        </div>
                      ) : (
                        <div className="flex items-center justify-center flex-1">
                          <span className={`text-xs font-mono font-semibold ${isHighlightPlacing ? "text-emerald-700" : "text-gray-300"}`}>
                            {isHighlightPlacing ? "Place Here" : slot.slot_id}
                          </span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Pending Storage List (col-span-4) */}
        <div className="lg:col-span-4 bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-5 flex flex-col gap-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <Clock className="size-4 text-gray-500" />
              <h3 className="text-base font-bold font-sans text-zinc-900">
                Pending Storage
              </h3>
            </div>
            <span className="px-2 py-0.5 rounded-full bg-slate-100 text-gray-700 font-bold text-xs font-mono">
              {pendingLots.length}
            </span>
          </div>

          {isLoading ? (
            <div className="py-12 flex flex-col items-center justify-center gap-2 text-gray-400">
              <Loader2 className="size-6 animate-spin text-sky-600" />
              <span className="text-xs font-sans">Memuat antrean...</span>
            </div>
          ) : pendingLots.length === 0 ? (
            <div className="py-12 flex flex-col items-center justify-center gap-2 text-gray-400 text-center">
              <CheckCircle2 className="size-8 text-emerald-500" />
              <span className="text-xs font-bold font-sans text-zinc-700">
                Semua lot PASS telah ditempatkan di slot!
              </span>
              <span className="text-[11px] font-sans text-gray-400">
                Jalankan inspeksi baru di menu Inspection.
              </span>
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {pendingLots.map((lot) => {
                const lid = lot.lotId || lot.lot_id || `LOT-${lot.id}`;
                const fam = lot.fishFamily || lot.fish_family || "Scombridae";
                const gr = lot.grade || "A";
                const confVal = Math.round(
                  lot.confidence !== undefined
                    ? lot.confidence > 1.0 ? lot.confidence : lot.confidence * 100
                    : (lot.grade_confidence ? lot.grade_confidence * 100 : 92.1)
                );

                const isCurrentlyPlacing = placingLot && (placingLot.lotId || placingLot.lot_id) === lid;

                return (
                  <div
                    key={lid}
                    className={`p-3.5 rounded-md border flex flex-col gap-2.5 transition-all ${
                      isCurrentlyPlacing
                        ? "bg-sky-50 border-sky-400 ring-2 ring-sky-300"
                        : "bg-slate-50/70 border-slate-200 hover:border-slate-300"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold font-mono text-zinc-900">
                        {lid}
                      </span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-sm ${
                          gr === "A"
                            ? "bg-green-100 text-green-800"
                            : "bg-amber-100 text-amber-800"
                        }`}
                      >
                        GRADE {gr}
                      </span>
                    </div>

                    <div className="text-xs font-sans text-gray-600 flex justify-between items-center">
                      <span>{fam}</span>
                      <span className="font-mono font-bold text-zinc-800">{confVal}% Confidence</span>
                    </div>

                    <span className="text-[11px] font-sans text-gray-400 italic">
                      Waiting for slot assignment
                    </span>

                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <button
                        type="button"
                        onClick={() => handleStartPlacing(lot, "cold")}
                        className={`py-1.5 px-2 rounded-sm text-xs font-bold font-sans transition-colors cursor-pointer ${
                          isCurrentlyPlacing && suggestedZone === "cold"
                            ? "bg-sky-700 text-white"
                            : "bg-sky-600 text-white hover:bg-sky-700 shadow-xs"
                        }`}
                      >
                        Assign to Cold
                      </button>
                      <button
                        type="button"
                        onClick={() => handleStartPlacing(lot, "frozen")}
                        className={`py-1.5 px-2 rounded-sm text-xs font-bold font-sans transition-colors cursor-pointer ${
                          isCurrentlyPlacing && suggestedZone === "frozen"
                            ? "bg-indigo-700 text-white"
                            : "bg-slate-100 text-zinc-800 border border-slate-300 hover:bg-slate-200"
                        }`}
                      >
                        Assign to Frozen
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          <div className="pt-3 border-t border-slate-100 text-center">
            <Link
              href="/history"
              className="text-xs font-bold font-sans text-sky-700 hover:text-sky-900 transition-colors inline-flex items-center gap-1"
            >
              <span>View All in Lot History</span>
              <ExternalLink className="size-3" />
            </Link>
          </div>
        </div>
      </div>

      {/* Drawer */}
      <SlotDetailDrawer
        slot={activeSlot}
        onClose={() => setActiveSlot(null)}
        onClearSlot={handleClearSlot}
        isClearing={isClearing}
      />
    </div>
  );
}
