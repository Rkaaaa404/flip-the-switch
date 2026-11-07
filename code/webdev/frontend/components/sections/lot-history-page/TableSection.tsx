"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight, Loader2, Inbox, Eye } from "lucide-react";
import { GradeBadge } from "@/components/common/GradeBadge";
import { StatusBadge } from "@/components/common/StatusBadge";
import { fetchLots } from "@/lib/api";
import { LotRecord } from "@/types";

type TableSectionProps = {
  search?: string;
  family?: string;
  grade?: string;
  decision?: string;
  dateFrom?: string;
  dateTo?: string;
};

function formatFullTimestamp(ts?: string): string {
  if (!ts) return "-";
  try {
    const d = new Date(ts);
    if (isNaN(d.getTime())) return ts;
    return d.toLocaleString("id-ID", {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return ts;
  }
}

export const TableSection = ({
  search = "",
  family = "all",
  grade = "all",
  decision = "all",
  dateFrom = "",
  dateTo = "",
}: TableSectionProps) => {
  const [lots, setLots] = useState<LotRecord[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [limit] = useState<number>(10);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetchLots({
        page,
        limit,
        search: search || undefined,
        family: family !== "all" ? family : undefined,
        grade: grade !== "all" ? grade : undefined,
        decision: decision !== "all" ? decision : undefined,
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
      });

      setLots(res.items || []);
      setTotal(res.total || 0);
      setTotalPages(res.total_pages || res.totalPages || 1);
    } catch (err) {
      console.warn("Failed to fetch lot records:", err);
      setLots([]);
      setTotal(0);
      setTotalPages(1);
    } finally {
      setIsLoading(false);
    }
  }, [page, limit, search, family, grade, decision, dateFrom, dateTo]);

  // Reset to page 1 whenever filters change
  useEffect(() => {
    setPage(1);
  }, [search, family, grade, decision, dateFrom, dateTo]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const passCount = lots.filter((l) => (l.decision || "").toUpperCase() === "PASS").length;
  const failCount = lots.filter((l) => (l.decision || "").toUpperCase() === "FAIL").length;

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Stats Summary Bar */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-200 text-xs font-sans text-gray-600">
        <div>
          <span>Menampilkan </span>
          <span className="font-bold text-zinc-900">{lots.length}</span>
          <span> dari </span>
          <span className="font-bold text-zinc-900">{total}</span>
          <span> rekaman log inspeksi</span>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-sm border border-emerald-200 font-medium">
            Lolos: {passCount}
          </span>
          <span className="text-rose-700 bg-rose-50 px-2 py-0.5 rounded-sm border border-rose-200 font-medium">
            Reject: {failCount}
          </span>
        </div>
      </div>

      {/* Table Card */}
      <div className="w-full bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 overflow-hidden">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="w-48 px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Lot ID
              </th>
              <th className="w-40 px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Timestamp
              </th>
              <th className="w-36 px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Jenis Ikan
              </th>
              <th className="w-24 px-4 py-3 text-center text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Grade (SNI)
              </th>
              <th className="w-36 px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Cacat Terdeteksi
              </th>
              <th className="w-32 px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Keputusan
              </th>
              <th className="w-24 px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Confidence
              </th>
              <th className="w-24 px-4 py-3 text-right text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                Aksi
              </th>
            </tr>
          </thead>

          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={8} className="px-4 py-16 text-center text-gray-500">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <Loader2 className="size-7 animate-spin text-sky-600" />
                    <span className="text-xs font-medium font-sans">Memuat data log inspeksi...</span>
                  </div>
                </td>
              </tr>
            ) : lots.length === 0 ? (
              <tr>
                <td colSpan={8} className="px-4 py-16 text-center text-gray-500">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <Inbox className="size-8 text-slate-300" />
                    <span className="text-sm font-semibold font-sans text-zinc-700">
                      Tidak ada catatan yang sesuai dengan filter.
                    </span>
                    <span className="text-xs font-sans text-gray-400">
                      Coba reset kata kunci pencarian atau jenis ikan.
                    </span>
                  </div>
                </td>
              </tr>
            ) : (
              lots.map((lot, index) => {
                const rowLotId = lot.lotId || lot.lot_id || `LOT-${lot.id}`;
                const rowFamily = lot.fishFamily || lot.fish_family || lot.family || "Tuna";
                const rowGrade = lot.grade || "A";
                const rowDecision = lot.decision || "PASS";
                const rowDefects = lot.defectsCount ?? lot.defects_count ?? (lot.defects ? lot.defects.length : 0);
                const rowConf = Math.round(
                  lot.confidence !== undefined
                    ? lot.confidence > 1.0 ? lot.confidence : lot.confidence * 100
                    : (lot.grade_confidence ? lot.grade_confidence * 100 : 90)
                );

                return (
                  <tr
                    key={rowLotId}
                    className={`${index !== 0 ? "border-t border-slate-100" : ""} hover:bg-slate-50 transition-colors`}
                  >
                    {/* Lot ID */}
                    <td className="px-4 py-3.5 w-48">
                      <Link
                        href={`/history/${rowLotId}`}
                        className="text-xs font-bold font-mono text-sky-600 hover:text-sky-800 hover:underline"
                      >
                        {rowLotId}
                      </Link>
                    </td>

                    {/* Timestamp */}
                    <td className="px-4 py-3.5 w-40 text-xs font-mono text-gray-600">
                      {formatFullTimestamp(lot.timestamp)}
                    </td>

                    {/* Fish Family */}
                    <td className="px-4 py-3.5 w-36">
                      <span className="text-xs font-medium font-sans text-zinc-800 bg-slate-100 px-2 py-0.5 rounded-sm border border-slate-200">
                        {rowFamily}
                      </span>
                    </td>

                    {/* Grade Badge */}
                    <td className="px-4 py-3.5 w-24 text-center">
                      <GradeBadge grade={rowGrade} />
                    </td>

                    {/* Defects Count */}
                    <td className="px-4 py-3.5 w-36">
                      <span
                        className={`text-xs font-mono px-2 py-0.5 rounded-sm font-semibold border ${
                          rowDefects > 0
                            ? "bg-rose-50 text-rose-700 border-rose-200"
                            : "bg-emerald-50 text-emerald-700 border-emerald-200"
                        }`}
                      >
                        {rowDefects} Cacat
                      </span>
                    </td>

                    {/* Decision */}
                    <td className="px-4 py-3.5 w-32">
                      <StatusBadge decision={rowDecision} />
                    </td>

                    {/* Confidence */}
                    <td className="px-4 py-3.5 w-24 text-xs font-bold font-mono text-zinc-900">
                      {rowConf}%
                    </td>

                    {/* Actions */}
                    <td className="px-4 py-3.5 w-24 text-right">
                      <Link
                        href={`/history/${rowLotId}`}
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-sm bg-slate-50 outline outline-1 outline-slate-300 text-xs font-semibold font-sans text-zinc-900 hover:bg-sky-50 hover:outline-sky-500 hover:text-sky-700 transition-colors cursor-pointer"
                      >
                        <Eye className="size-3" />
                        <span>Detail</span>
                      </Link>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>

        {/* Pagination Footer */}
        <div className="px-4 py-3 bg-slate-50/80 border-t border-slate-200 flex items-center justify-between">
          <span className="text-xs font-sans text-gray-500">
            Halaman <span className="font-bold text-zinc-900">{page}</span> dari{" "}
            <span className="font-bold text-zinc-900">{Math.max(1, totalPages)}</span>
          </span>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1 || isLoading}
              className="p-1.5 rounded-sm border border-slate-300 bg-white text-gray-700 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer transition-colors"
            >
              <ChevronLeft className="size-4" />
            </button>

            <button
              type="button"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages || isLoading}
              className="p-1.5 rounded-sm border border-slate-300 bg-white text-gray-700 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer transition-colors"
            >
              <ChevronRight className="size-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
