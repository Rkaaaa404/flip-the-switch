"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { ClipboardList, ArrowRight, Loader2, Inbox } from "lucide-react";
import { GradeBadge } from "@/components/common/GradeBadge";
import { StatusBadge } from "@/components/common/StatusBadge";
import { fetchRecentLots } from "@/lib/api";
import { LotRecord } from "@/types";

interface RecentInspectionsProps {
  lots?: LotRecord[] | null;
  isLoading?: boolean;
}

const TH_CLASS = "px-4 py-2 text-left text-xs font-medium font-sans uppercase tracking-wide text-gray-700";

function formatTimestampTime(ts?: string): string {
  if (!ts) return "Baru saja";
  try {
    const d = new Date(ts);
    if (isNaN(d.getTime())) {
      return ts.includes("T") ? ts.split("T")[1]?.slice(0, 8) : ts;
    }
    return d.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch {
    return ts;
  }
}

export const RecentInspections = ({ lots: propLots, isLoading = false }: RecentInspectionsProps) => {
  const [internalLots, setInternalLots] = useState<LotRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (propLots !== undefined) return;

    let isMounted = true;
    const loadRecent = async () => {
      try {
        setLoading(true);
        const data = await fetchRecentLots(5);
        if (isMounted) setInternalLots(data);
      } catch (err) {
        console.warn("Failed to fetch recent lots:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadRecent();
    return () => {
      isMounted = false;
    };
  }, [propLots]);

  const activeLots = propLots !== undefined ? (propLots || []) : internalLots;
  const isFetching = isLoading || (loading && activeLots.length === 0);

  return (
    <div className="flex-1 self-stretch bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-offset-[-1px] outline-slate-300 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-200 flex justify-between items-center bg-slate-50/50">
        <div className="flex items-center gap-2">
          <ClipboardList className="size-4 text-sky-700" />
          <span className="text-base font-bold font-sans text-zinc-900">Recent Inspections (Live Feed)</span>
        </div>
        <span className="text-xs font-mono text-gray-500 font-medium">
          {activeLots.length} lot terakhir
        </span>
      </div>

      {/* Table */}
      <div className="flex-1 overflow-auto min-h-[300px]">
        {isFetching ? (
          <div className="h-full flex flex-col items-center justify-center gap-2 text-gray-500 py-12">
            <Loader2 className="size-6 animate-spin text-sky-500" />
            <span className="text-xs font-sans">Memuat riwayat inspeksi terbaru...</span>
          </div>
        ) : activeLots.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center gap-2 text-gray-500 py-12">
            <Inbox className="size-8 text-slate-300" />
            <p className="text-sm font-medium font-sans text-zinc-700">Belum ada inspeksi yang dicatat hari ini.</p>
            <p className="text-xs font-sans text-gray-400">Jalankan inspeksi di menu &quot;Inspection&quot; untuk melihat log QC di sini.</p>
          </div>
        ) : (
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/80">
                <th className={`${TH_CLASS} w-44`}>Lot ID</th>
                <th className={`${TH_CLASS} w-24 text-center`}>Grade</th>
                <th className={`${TH_CLASS} w-28`}>Decision</th>
                <th className={`${TH_CLASS} w-28`}>Confidence</th>
                <th className={`${TH_CLASS} w-28 text-right`}>Waktu</th>
              </tr>
            </thead>
            <tbody>
              {activeLots.map((row, i) => {
                const rowLotId = row.lotId || row.lot_id || `LOT-${row.id}`;
                const rowGrade = row.grade || "A";
                const rowDecision = row.decision || "PASS";
                const rowConf = Math.round(
                  row.confidence !== undefined
                    ? row.confidence > 1.0 ? row.confidence : row.confidence * 100
                    : (row.grade_confidence ? row.grade_confidence * 100 : 90)
                );

                return (
                  <tr
                    key={rowLotId}
                    className={`${i !== 0 ? "border-t border-slate-100" : ""} hover:bg-slate-50/80 transition-colors`}
                  >
                    <td className="px-4 py-3.5 w-44">
                      <Link
                        href={`/history/${rowLotId}`}
                        className="text-xs font-bold font-mono text-sky-600 hover:text-sky-800 hover:underline"
                      >
                        {rowLotId}
                      </Link>
                    </td>
                    <td className="px-4 py-3 w-24 text-center">
                      <GradeBadge grade={rowGrade} />
                    </td>
                    <td className="px-4 py-3 w-28">
                      <StatusBadge decision={rowDecision} />
                    </td>
                    <td className="px-4 py-3.5 w-28 text-xs font-semibold font-mono text-zinc-900">
                      {rowConf}%
                    </td>
                    <td className="px-4 py-3.5 w-28 text-xs font-mono text-gray-500 text-right">
                      {formatTimestampTime(row.timestamp)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Footer */}
      <div className="px-4 py-2.5 border-t border-slate-200 bg-slate-50/50 flex justify-end items-center">
        <Link
          href="/history"
          className="text-xs font-bold font-sans tracking-wide text-sky-700 hover:text-sky-900 transition-colors flex items-center gap-1"
        >
          <span>LIHAT SELURUH RIWAYAT (AUDIT LOG)</span>
          <ArrowRight className="size-3" />
        </Link>
      </div>
    </div>
  );
};
