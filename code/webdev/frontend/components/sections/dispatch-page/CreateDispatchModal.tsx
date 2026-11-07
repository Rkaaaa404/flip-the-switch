"use client";

import React, { useEffect, useState } from "react";
import { X, Info, Loader2, Check, AlertCircle } from "lucide-react";
import { fetchAvailableLotsForDispatch, createDispatch } from "@/lib/api";
import { LotRecord } from "@/types";

interface CreateDispatchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: () => void;
}

const COUNTRIES = [
  { code: "USA", label: "USA 🇺🇸" },
  { code: "Japan", label: "Japan 🇯🇵" },
  { code: "China", label: "China 🇨🇳" },
  { code: "EU", label: "EU 🇪🇺" },
  { code: "Singapore", label: "Singapore 🇸🇬" },
  { code: "Australia", label: "Australia 🇦🇺" },
  { code: "South Korea", label: "South Korea 🇰🇷" },
  { code: "Vietnam", label: "Vietnam 🇻🇳" },
  { code: "Malaysia", label: "Malaysia 🇲🇾" },
];

export const CreateDispatchModal = ({
  isOpen,
  onClose,
  onCreated,
}: CreateDispatchModalProps) => {
  const [buyerName, setBuyerName] = useState("");
  const [destination, setDestination] = useState("USA");
  const [containerNo, setContainerNo] = useState("");
  const [dispatchDate, setDispatchDate] = useState("");
  const [notes, setNotes] = useState("");

  const [availableLots, setAvailableLots] = useState<LotRecord[]>([]);
  const [selectedLotIds, setSelectedLotIds] = useState<string[]>([]);
  const [isLoadingLots, setIsLoadingLots] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Default to now formatted as YYYY-MM-DDTHH:MM
      const now = new Date();
      const localIso = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
        .toISOString()
        .slice(0, 16);
      setDispatchDate(localIso);

      // Load available lots
      setIsLoadingLots(true);
      setErrorMsg(null);
      fetchAvailableLotsForDispatch()
        .then((lots) => {
          setAvailableLots(lots);
          // Pre-select first 2 lots if available for quick convenience
          if (lots.length > 0) {
            setSelectedLotIds(lots.slice(0, Math.min(2, lots.length)).map((l) => l.lotId || l.lot_id || `LOT-${l.id}`));
          }
        })
        .catch((err) => {
          console.warn("Failed to load lots for dispatch:", err);
        })
        .finally(() => {
          setIsLoadingLots(false);
        });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const toggleLotSelection = (lotId: string) => {
    setSelectedLotIds((prev) =>
      prev.includes(lotId) ? prev.filter((id) => id !== lotId) : [...prev, lotId]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!buyerName.trim()) {
      setErrorMsg("Nama Buyer / Perusahaan wajib diisi.");
      return;
    }
    if (selectedLotIds.length === 0) {
      setErrorMsg("Pilih minimal 1 lot ikan untuk pengiriman.");
      return;
    }

    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await createDispatch({
        buyer_name: buyerName,
        destination,
        container_no: containerNo || undefined,
        dispatch_date: dispatchDate || undefined,
        lot_ids: selectedLotIds,
        notes: notes || undefined,
      });

      // Reset form and notify parent
      setBuyerName("");
      setContainerNo("");
      setNotes("");
      setSelectedLotIds([]);
      onCreated();
      onClose();
    } catch (err: any) {
      setErrorMsg(err?.message || "Gagal membuat catatan pengiriman.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-in fade-in duration-200">
      <div className="w-full max-w-xl bg-white rounded-xl shadow-2xl border border-slate-200 flex flex-col max-h-[90vh] overflow-hidden animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-xl font-bold font-sans text-zinc-900">
            Create New Dispatch
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-sm text-gray-400 hover:text-zinc-900 hover:bg-slate-100 transition-colors cursor-pointer"
          >
            <X className="size-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto flex flex-col gap-5 flex-1">
          {errorMsg && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-md flex items-center gap-2 text-sm text-red-700">
              <AlertCircle className="size-4 shrink-0 text-red-600" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* SHIPMENT INFO SECTION */}
          <div className="flex flex-col gap-3">
            <span className="text-[11px] font-bold font-mono text-gray-500 uppercase tracking-wider">
              SHIPMENT INFO
            </span>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {/* Buyer Name */}
              <div className="flex flex-col gap-1">
                <label className="text-xs font-semibold text-zinc-800">
                  Buyer / Company Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={buyerName}
                  onChange={(e) => setBuyerName(e.target.value)}
                  placeholder="e.g. PT Rahayu Seafood"
                  className="px-3 py-2 bg-slate-50 rounded-sm border border-slate-300 text-sm font-sans text-zinc-900 focus:outline-sky-500"
                />
              </div>

              {/* Destination */}
              <div className="flex flex-col gap-1">
                <label className="text-xs font-semibold text-zinc-800">
                  Destination Country
                </label>
                <select
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  className="px-3 py-2 bg-slate-50 rounded-sm border border-slate-300 text-sm font-sans text-zinc-900 cursor-pointer focus:outline-sky-500"
                >
                  {COUNTRIES.map((c) => (
                    <option key={c.code} value={c.code}>
                      {c.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Container Number */}
              <div className="flex flex-col gap-1">
                <label className="text-xs font-semibold text-zinc-800">
                  Container Number
                </label>
                <input
                  type="text"
                  value={containerNo}
                  onChange={(e) => setContainerNo(e.target.value)}
                  placeholder="CONT-2026-001 (optional)"
                  className="px-3 py-2 bg-slate-50 rounded-sm border border-slate-300 text-sm font-sans text-zinc-900 focus:outline-sky-500"
                />
              </div>

              {/* Dispatch Date */}
              <div className="flex flex-col gap-1">
                <label className="text-xs font-semibold text-zinc-800">
                  Dispatch Date & Time
                </label>
                <input
                  type="datetime-local"
                  value={dispatchDate}
                  onChange={(e) => setDispatchDate(e.target.value)}
                  className="px-3 py-2 bg-slate-50 rounded-sm border border-slate-300 text-sm font-sans text-zinc-900 focus:outline-sky-500"
                />
              </div>
            </div>

            {/* Inspector Notes */}
            <div className="flex flex-col gap-1">
              <label className="text-xs font-semibold text-zinc-800">
                Inspector Notes
              </label>
              <textarea
                rows={2}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Optional notes about this shipment (e.g. IQF frozen, HACCP batch check)"
                className="px-3 py-2 bg-slate-50 rounded-sm border border-slate-300 text-sm font-sans text-zinc-900 focus:outline-sky-500 resize-none"
              />
            </div>
          </div>

          {/* SELECT LOTS FROM STORAGE SECTION */}
          <div className="flex flex-col gap-2 pt-2 border-t border-slate-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-bold font-mono text-gray-500 uppercase tracking-wider">
                  SELECT LOTS FROM STORAGE
                </span>
                <Info className="size-3.5 text-gray-400" />
              </div>
              <span className="text-xs font-sans text-gray-400">
                Only stored lots that haven't been dispatched are shown
              </span>
            </div>

            {/* Lots List Box */}
            <div className="border border-slate-200 rounded-md overflow-hidden max-h-48 overflow-y-auto divide-y divide-slate-100 bg-white">
              {isLoadingLots ? (
                <div className="p-6 flex flex-col items-center justify-center gap-2 text-gray-400">
                  <Loader2 className="size-5 animate-spin text-sky-600" />
                  <span className="text-xs font-sans">Memuat lot yang tersedia...</span>
                </div>
              ) : availableLots.length === 0 ? (
                <div className="p-6 text-center text-xs font-sans text-gray-500">
                  Tidak ada lot yang tersimpan di storage saat ini. Lakukan inspeksi dan tempatkan ke storage terlebih dahulu.
                </div>
              ) : (
                availableLots.map((lot) => {
                  const lid = lot.lotId || lot.lot_id || `LOT-${lot.id}`;
                  const isChecked = selectedLotIds.includes(lid);
                  const fam = lot.fishFamily || lot.fish_family || "Tuna";
                  const gr = lot.grade || "A";
                  const confVal = Math.round(
                    lot.confidence !== undefined
                      ? lot.confidence > 1.0 ? lot.confidence : lot.confidence * 100
                      : (lot.grade_confidence ? lot.grade_confidence * 100 : 90)
                  );

                  return (
                    <div
                      key={lid}
                      onClick={() => toggleLotSelection(lid)}
                      className={`px-3.5 py-2.5 flex items-center justify-between gap-3 text-xs font-sans transition-colors cursor-pointer ${
                        isChecked ? "bg-sky-50/70" : "hover:bg-slate-50"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => {}} // handled by div onClick
                          className="size-4 text-sky-600 rounded-xs border-slate-300 accent-sky-600 cursor-pointer"
                        />
                        <span className="font-bold font-mono text-zinc-900">{lid}</span>
                        <span className="text-gray-600">{fam}</span>
                      </div>

                      <div className="flex items-center gap-3">
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-sm ${
                            gr === "A"
                              ? "bg-green-100 text-green-800"
                              : "bg-amber-100 text-amber-800"
                          }`}
                        >
                          GRADE {gr}
                        </span>
                        <span className="font-mono font-bold text-zinc-800">{confVal}%</span>
                        <span className="text-gray-400 text-[11px]">{lot.storageSlot || "Cold Zone"}</span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>

            {/* Selected Count Indicator */}
            <span className="text-xs font-semibold text-sky-700">
              {selectedLotIds.length} {selectedLotIds.length === 1 ? "lot" : "lots"} selected
            </span>
          </div>

          {/* Footer Buttons */}
          <div className="pt-4 border-t border-slate-200 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-sm border border-slate-300 bg-white text-zinc-700 font-bold text-xs font-sans hover:bg-slate-50 transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || selectedLotIds.length === 0}
              className="px-5 py-2 rounded-sm bg-sky-600 text-white font-bold text-xs font-sans hover:bg-sky-700 disabled:opacity-50 transition-colors cursor-pointer shadow-xs flex items-center gap-1.5"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="size-3.5 animate-spin" />
                  <span>Creating...</span>
                </>
              ) : (
                <span>Create Dispatch</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
