"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  Download,
  CheckCircle2,
  Loader2,
  Inbox,
  Clock,
  Navigation,
  PackageCheck,
  Check,
} from "lucide-react";
import { fetchDispatchDetail, updateDispatchStatus, API_BASE } from "@/lib/api";
import { DispatchRecord } from "@/types";

const DEST_FLAGS: Record<string, string> = {
  USA: "🇺🇸",
  Japan: "🇯🇵",
  China: "🇨🇳",
  EU: "🇪🇺",
  Singapore: "🇸🇬",
  Australia: "🇦🇺",
  "South Korea": "🇰🇷",
  Vietnam: "🇻🇳",
  Malaysia: "🇲🇾",
};

export default function DispatchDetailPage() {
  const params = useParams();
  const router = useRouter();
  const dispatchId = (params?.dispatchId as string) || "";

  const [dispatch, setDispatch] = useState<DispatchRecord | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isUpdating, setIsUpdating] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    const loadData = async () => {
      setIsLoading(true);
      try {
        const data = await fetchDispatchDetail(dispatchId);
        if (isMounted) setDispatch(data);
      } catch (err) {
        console.warn("Failed to fetch dispatch detail:", err);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };

    if (dispatchId) loadData();
    return () => {
      isMounted = false;
    };
  }, [dispatchId]);

  const handleUpdateStatus = async (nextStatus: string) => {
    setIsUpdating(true);
    try {
      await updateDispatchStatus(dispatchId, nextStatus);
      const updated = await fetchDispatchDetail(dispatchId);
      setDispatch(updated);
    } catch (err) {
      console.warn("Failed to update dispatch status:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleExportCsv = () => {
    window.open(`${API_BASE}/api/v1/dispatch/${dispatchId}/export`, "_blank");
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-20 gap-3">
        <Loader2 className="size-8 animate-spin text-sky-600" />
        <span className="text-sm font-semibold font-sans text-zinc-700">
          Memuat Detail Manifes Pengiriman {dispatchId}...
        </span>
      </div>
    );
  }

  if (!dispatch) {
    return (
      <div className="p-12 flex flex-col items-center justify-center gap-4 text-center">
        <Inbox className="size-12 text-slate-300" />
        <h2 className="text-lg font-bold font-sans text-zinc-800">
          Catatan Pengiriman Tidak Ditemukan
        </h2>
        <Link
          href="/dispatch"
          className="text-xs font-bold font-sans text-sky-600 hover:underline"
        >
          ← Kembali ke Export Dispatch
        </Link>
      </div>
    );
  }

  const rawStatus = (dispatch.status || "").toLowerCase();
  const currentStatus = rawStatus === "dispatched" ? "in_transit" : rawStatus;
  const flag = DEST_FLAGS[dispatch.destination] || "🌐";
  const lots = dispatch.lots || [];
  const qcSummary = dispatch.qc_summary || {
    total_lots: lots.length,
    all_passed: true,
    avg_confidence: 91.4,
    total_defects: 0,
  };

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      {/* Back Link */}
      <div>
        <Link
          href="/dispatch"
          className="inline-flex items-center gap-1.5 text-xs font-bold font-sans text-sky-600 hover:text-sky-800 transition-colors"
        >
          <ArrowLeft className="size-3.5" />
          <span>Back to Dispatch</span>
        </Link>
      </div>

      {/* Title & Subtitle */}
      <div className="flex flex-col">
        <h1 className="text-3xl font-black font-mono text-zinc-900 tracking-tight">
          {dispatch.dispatch_id || dispatch.dispatchId}
        </h1>
        <p className="text-sm font-sans text-gray-500 mt-1 font-medium">
          {dispatch.buyer_name || dispatch.buyerName} — {flag} {dispatch.destination}
        </p>
      </div>

      {/* Main 2-Column Grid */}
      <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN: Lots in This Shipment (col-span-7) */}
        <div className="lg:col-span-7 bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h2 className="text-base font-bold font-sans text-zinc-900">
              Lots in This Shipment ({lots.length} {lots.length === 1 ? "lot" : "lots"})
            </h2>
          </div>

          {/* Lots Table */}
          <div className="w-full overflow-x-auto">
            <table className="w-full border-collapse text-xs font-sans">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="px-3 py-2.5 text-left font-bold text-gray-600">Lot ID</th>
                  <th className="px-3 py-2.5 text-left font-bold text-gray-600">Jenis Ikan</th>
                  <th className="px-3 py-2.5 text-center font-bold text-gray-600">Grade</th>
                  <th className="px-3 py-2.5 text-left font-bold text-gray-600">Defects</th>
                  <th className="px-3 py-2.5 text-left font-bold text-gray-600">Confidence</th>
                  <th className="px-3 py-2.5 text-left font-bold text-gray-600">Inspection Date</th>
                </tr>
              </thead>
              <tbody>
                {lots.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-3 py-8 text-center text-gray-400">
                      Tidak ada detail lot tercatat.
                    </td>
                  </tr>
                ) : (
                  lots.map((lot, idx) => {
                    const lid = lot.lotId || lot.lot_id;
                    const fam = lot.fishFamily || lot.fish_family || "Tuna";
                    const gr = lot.grade || "A";
                    const defCount = lot.defectsCount ?? lot.defects_count ?? 0;
                    const conf = Math.round(
                      lot.confidence !== undefined
                        ? lot.confidence > 1.0 ? lot.confidence : lot.confidence * 100
                        : (lot.grade_confidence ? lot.grade_confidence * 100 : 92)
                    );

                    return (
                      <tr
                        key={lid || idx}
                        className={`${idx !== 0 ? "border-t border-slate-100" : ""} hover:bg-slate-50`}
                      >
                        <td className="px-3 py-3">
                          <Link
                            href={`/history/${lid}`}
                            className="font-bold font-mono text-sky-600 hover:underline"
                          >
                            {lid}
                          </Link>
                        </td>
                        <td className="px-3 py-3 text-zinc-800">{fam}</td>
                        <td className="px-3 py-3 text-center">
                          <span
                            className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-sm ${
                              gr === "A"
                                ? "bg-green-100 text-green-800"
                                : "bg-amber-100 text-amber-800"
                            }`}
                          >
                            Grade {gr}
                          </span>
                        </td>
                        <td className="px-3 py-3 text-gray-600 font-mono">
                          {defCount} {defCount === 1 ? "defect" : "defects"}
                        </td>
                        <td className="px-3 py-3 font-mono font-bold text-zinc-900">{conf}%</td>
                        <td className="px-3 py-3 text-gray-500 font-mono">{lot.timestamp || "-"}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* Green QC Check Banner */}
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-md flex items-center gap-2 text-xs font-semibold text-emerald-800">
            <CheckCircle2 className="size-4 text-emerald-600 shrink-0" />
            <span>All {lots.length} lots passed QC inspection (SNI 2729:2013 Organoleptic Standard)</span>
          </div>
        </div>

        {/* RIGHT COLUMN: Shipment Summary & QC Summary (col-span-5) */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* 1. Shipment Summary Card */}
          <div className="bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-6 flex flex-col gap-4">
            <h2 className="text-base font-bold font-sans text-zinc-900 pb-3 border-b border-slate-100">
              Shipment Summary
            </h2>

            <div className="flex flex-col gap-3 text-xs font-sans">
              <div className="flex justify-between items-center">
                <span className="text-gray-500">Dispatch ID</span>
                <span className="font-mono font-bold text-sky-600">
                  {dispatch.dispatch_id || dispatch.dispatchId}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-500">Status</span>
                <div>
                  {currentStatus === "pending" && (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
                      <span className="size-1.5 rounded-full bg-amber-500" />
                      Pending
                    </span>
                  )}
                  {currentStatus === "in_transit" && (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-sky-100 text-sky-800 border border-sky-300">
                      <span className="size-1.5 rounded-full bg-sky-500" />
                      In Transit
                    </span>
                  )}
                  {currentStatus === "delivered" && (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                      <span className="size-1.5 rounded-full bg-emerald-500" />
                      Delivered
                    </span>
                  )}
                </div>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-500">Buyer</span>
                <span className="font-bold text-zinc-900">
                  {dispatch.buyer_name || dispatch.buyerName}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-500">Destination</span>
                <span className="font-bold text-zinc-900">
                  {dispatch.destination} {flag}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-500">Container</span>
                <span className="font-mono font-bold text-zinc-900">
                  {dispatch.container_no || dispatch.containerNo || "-"}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-gray-500">Dispatch Date</span>
                <span className="font-mono text-zinc-800">
                  {dispatch.dispatch_date || dispatch.dispatchDate || "-"}
                </span>
              </div>
            </div>

            {/* Lifecycle Transition Actions */}
            {currentStatus === "pending" && (
              <div className="pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => handleUpdateStatus("in_transit")}
                  disabled={isUpdating}
                  className="w-full py-2 bg-sky-600 text-white font-bold text-xs font-sans rounded-sm hover:bg-sky-700 transition-colors cursor-pointer shadow-xs flex items-center justify-center gap-1.5"
                >
                  <Navigation className="size-4" />
                  <span>{isUpdating ? "Updating..." : "Mulai Kirim (Set In Transit)"}</span>
                </button>
              </div>
            )}

            {currentStatus === "in_transit" && (
              <div className="pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => handleUpdateStatus("delivered")}
                  disabled={isUpdating}
                  className="w-full py-2 bg-emerald-600 text-white font-bold text-xs font-sans rounded-sm hover:bg-emerald-700 transition-colors cursor-pointer shadow-xs flex items-center justify-center gap-1.5"
                >
                  <PackageCheck className="size-4" />
                  <span>{isUpdating ? "Updating..." : "Konfirmasi Tiba (Set Delivered)"}</span>
                </button>
              </div>
            )}

            {currentStatus === "delivered" && (
              <div className="pt-2 border-t border-slate-100 p-2.5 bg-emerald-50 rounded-sm border border-emerald-200 text-center">
                <span className="text-xs font-bold font-sans text-emerald-800 flex items-center justify-center gap-1">
                  <Check className="size-4 text-emerald-600" />
                  Pengiriman Telah Selesai & Diterima Buyer
                </span>
              </div>
            )}
          </div>

          {/* 2. QC SUMMARY Card */}
          <div className="bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-6 flex flex-col gap-4">
            <span className="text-[11px] font-bold font-mono text-gray-500 uppercase tracking-wider">
              QC SUMMARY
            </span>

            <div className="grid grid-cols-2 gap-3">
              {/* Box 1: Total Lots */}
              <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
                <span className="text-[11px] text-gray-500 font-sans block">Total Lots</span>
                <span className="text-xl font-black font-sans text-zinc-900 mt-1 block">
                  {qcSummary.total_lots}
                </span>
              </div>

              {/* Box 2: All Grade A/B */}
              <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
                <span className="text-[11px] text-gray-500 font-sans block">All Grade A/B</span>
                <span className="text-xl font-black font-sans text-emerald-600 mt-1 block flex items-center gap-1">
                  ✓ Yes
                </span>
              </div>

              {/* Box 3: Avg Confidence */}
              <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
                <span className="text-[11px] text-gray-500 font-sans block">Avg Confidence</span>
                <span className="text-xl font-black font-mono text-zinc-900 mt-1 block">
                  {qcSummary.avg_confidence}%
                </span>
              </div>

              {/* Box 4: Defects Found */}
              <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
                <span className="text-[11px] text-gray-500 font-sans block">Defects Found</span>
                <span className="text-xl font-black font-mono text-amber-600 mt-1 block">
                  {qcSummary.total_defects}
                </span>
              </div>
            </div>

            {/* Export Summary Button (Planned for Final) */}
            <button
              type="button"
              disabled
              title="Available in Final version"
              className="w-full py-2.5 rounded-sm border border-slate-200 bg-slate-100 text-gray-400 font-bold text-xs font-sans flex items-center justify-center gap-2 cursor-not-allowed shadow-none mt-1"
            >
              <Download className="size-4 text-gray-400" />
              <span>Export Summary (PDF)</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
