"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  Truck,
  Clock,
  CheckCircle2,
  Navigation,
  Search,
  Plus,
  ChevronDown,
  Loader2,
  Inbox,
  Check,
  PackageCheck,
} from "lucide-react";
import { fetchDispatches, updateDispatchStatus } from "@/lib/api";
import { DispatchRecord } from "@/types";
import { CreateDispatchModal } from "@/components/sections/dispatch-page/CreateDispatchModal";

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

export default function DispatchPage() {
  const [dispatches, setDispatches] = useState<DispatchRecord[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [pendingCount, setPendingCount] = useState<number>(0);
  const [inTransitCount, setInTransitCount] = useState<number>(0);
  const [deliveredCount, setDeliveredCount] = useState<number>(0);

  const [search, setSearch] = useState<string>("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [isUpdatingStatus, setIsUpdatingStatus] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await fetchDispatches();
      setDispatches(data.items || []);
      setTotalCount(data.total_dispatches ?? data.totalDispatches ?? 0);
      setPendingCount(data.pending ?? 0);
      setInTransitCount(data.in_transit ?? data.inTransit ?? data.dispatched ?? 0);
      setDeliveredCount(data.delivered ?? 0);
    } catch (err) {
      console.warn("Failed to load dispatches:", err);
      setDispatches([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAdvanceStatus = async (dispatchId: string, currentStatus: string) => {
    setIsUpdatingStatus(dispatchId);
    try {
      const nextStatus = currentStatus === "pending" ? "in_transit" : "delivered";
      await updateDispatchStatus(dispatchId, nextStatus);
      await loadData();
    } catch (err) {
      console.warn("Failed to update status:", err);
    } finally {
      setIsUpdatingStatus(null);
    }
  };

  // Filtered dispatches
  const filteredDispatches = dispatches.filter((d) => {
    const q = search.toLowerCase();
    const matchSearch =
      !search ||
      d.dispatch_id.toLowerCase().includes(q) ||
      d.buyer_name.toLowerCase().includes(q) ||
      d.destination.toLowerCase().includes(q) ||
      (d.container_no && d.container_no.toLowerCase().includes(q));

    const s = d.status.toLowerCase();
    const normalizedStatus = s === "dispatched" ? "in_transit" : s;
    const matchStatus =
      statusFilter === "all" || normalizedStatus === statusFilter.toLowerCase();

    return matchSearch && matchStatus;
  });

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      {/* Top 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Total Dispatches */}
        <div className="p-5 bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 flex items-center gap-4">
          <div className="size-11 rounded-full bg-slate-100 flex items-center justify-center text-slate-700">
            <Truck className="size-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider font-mono">
              TOTAL DISPATCHES
            </span>
            <span className="text-2xl font-black font-sans text-zinc-900 block mt-0.5">
              {totalCount}
            </span>
          </div>
        </div>

        {/* Card 2: Pending */}
        <div className="p-5 bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 flex items-center gap-4">
          <div className="size-11 rounded-full bg-amber-50 flex items-center justify-center text-amber-600 border border-amber-200">
            <Clock className="size-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-amber-700 uppercase tracking-wider font-mono">
              PENDING
            </span>
            <span className="text-2xl font-black font-sans text-amber-700 block mt-0.5">
              {pendingCount}
            </span>
          </div>
        </div>

        {/* Card 3: In Transit */}
        <div className="p-5 bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 flex items-center gap-4">
          <div className="size-11 rounded-full bg-sky-50 flex items-center justify-center text-sky-600 border border-sky-200">
            <Navigation className="size-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-sky-700 uppercase tracking-wider font-mono">
              IN TRANSIT
            </span>
            <span className="text-2xl font-black font-sans text-sky-700 block mt-0.5">
              {inTransitCount}
            </span>
          </div>
        </div>

        {/* Card 4: Delivered */}
        <div className="p-5 bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 flex items-center gap-4">
          <div className="size-11 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 border border-emerald-200">
            <PackageCheck className="size-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider font-mono">
              DELIVERED
            </span>
            <span className="text-2xl font-black font-sans text-emerald-700 block mt-0.5">
              {deliveredCount}
            </span>
          </div>
        </div>
      </div>

      {/* Main Records Section */}
      <div className="w-full bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-6 flex flex-col gap-5">
        {/* Controls Row */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-100">
          <h2 className="text-lg font-black font-sans text-zinc-900 tracking-tight">
            Dispatch Records
          </h2>

          <div className="flex flex-wrap items-center gap-3">
            {/* Search Input */}
            <div className="relative min-w-[220px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-gray-400 pointer-events-none" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search dispatches..."
                className="w-full pl-9 pr-3 py-1.5 bg-slate-50 rounded-sm border border-slate-300 text-xs font-sans text-zinc-900 focus:outline-sky-500"
              />
            </div>

            {/* Status Dropdown */}
            <div className="relative min-w-[140px]">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-3 py-1.5 bg-slate-50 rounded-sm border border-slate-300 text-xs font-sans font-medium text-zinc-900 appearance-none pr-8 cursor-pointer focus:outline-sky-500"
              >
                <option value="all" className="font-sans text-zinc-900">All Status</option>
                <option value="pending" className="font-sans text-zinc-900">Pending</option>
                <option value="in_transit" className="font-sans text-zinc-900">In Transit</option>
                <option value="delivered" className="font-sans text-zinc-900">Delivered</option>
              </select>
              <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 size-3.5 text-gray-400 pointer-events-none" />
            </div>

            {/* New Dispatch Button */}
            <button
              type="button"
              onClick={() => setIsModalOpen(true)}
              className="flex items-center gap-1.5 px-4 py-1.5 bg-sky-600 text-white rounded-sm font-bold text-xs font-sans hover:bg-sky-700 transition-colors shadow-xs cursor-pointer"
            >
              <Plus className="size-4 stroke-[3]" />
              <span>New Dispatch</span>
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="w-full overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Dispatch ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Buyer
                </th>
                <th className="px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Destination
                </th>
                <th className="px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Lots
                </th>
                <th className="px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Date
                </th>
                <th className="px-4 py-3 text-left text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Status
                </th>
                <th className="px-4 py-3 text-right text-xs font-bold font-sans uppercase tracking-wider text-gray-600">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="px-4 py-16 text-center text-gray-500">
                    <div className="flex flex-col items-center justify-center gap-2">
                      <Loader2 className="size-6 animate-spin text-sky-600" />
                      <span className="text-xs font-medium font-sans">Memuat catatan pengiriman...</span>
                    </div>
                  </td>
                </tr>
              ) : filteredDispatches.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-16 text-center text-gray-500">
                    <div className="flex flex-col items-center justify-center gap-2">
                      <Inbox className="size-8 text-slate-300" />
                      <span className="text-sm font-semibold font-sans text-zinc-700">
                        Belum ada catatan pengiriman yang sesuai.
                      </span>
                      <span className="text-xs font-sans text-gray-400">
                        Klik "+ New Dispatch" untuk membuat catatan ekspor baru.
                      </span>
                    </div>
                  </td>
                </tr>
              ) : (
                filteredDispatches.map((disp, idx) => {
                  const did = disp.dispatch_id || disp.dispatchId || "";
                  const rawStatus = (disp.status || "").toLowerCase();
                  const currentStatus = rawStatus === "dispatched" ? "in_transit" : rawStatus;
                  const flag = DEST_FLAGS[disp.destination] || "🌐";

                  return (
                    <tr
                      key={did}
                      className={`${idx !== 0 ? "border-t border-slate-100" : ""} hover:bg-slate-50 transition-colors text-xs font-sans`}
                    >
                      {/* Dispatch ID */}
                      <td className="px-4 py-3.5">
                        <Link
                          href={`/dispatch/${did}`}
                          className="font-bold font-mono text-sky-600 hover:text-sky-800 hover:underline"
                        >
                          {did}
                        </Link>
                      </td>

                      {/* Buyer */}
                      <td className="px-4 py-3.5 font-medium text-zinc-900">
                        {disp.buyer_name || disp.buyerName}
                      </td>

                      {/* Destination */}
                      <td className="px-4 py-3.5">
                        <span className="inline-flex items-center gap-1.5 text-zinc-800 font-medium">
                          <span>{flag}</span>
                          <span>{disp.destination}</span>
                        </span>
                      </td>

                      {/* Lots */}
                      <td className="px-4 py-3.5 font-mono text-gray-600">
                        {disp.lots_count ?? disp.lotsCount ?? 1} lots
                      </td>

                      {/* Date */}
                      <td className="px-4 py-3.5 font-mono text-gray-600">
                        {disp.dispatch_date || disp.dispatchDate || "-"}
                      </td>

                      {/* Status Badge */}
                      <td className="px-4 py-3.5">
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
                      </td>

                      {/* Actions */}
                      <td className="px-4 py-3.5 text-right">
                        <div className="inline-flex items-center gap-2 justify-end">
                          {currentStatus === "pending" && (
                            <button
                              type="button"
                              onClick={() => handleAdvanceStatus(did, "pending")}
                              disabled={isUpdatingStatus === did}
                              className="px-2.5 py-1 rounded-sm bg-sky-50 border border-sky-300 text-sky-700 font-semibold hover:bg-sky-100 transition-colors text-[11px] flex items-center gap-1 cursor-pointer"
                            >
                              <Navigation className="size-3" />
                              <span>In Transit</span>
                            </button>
                          )}
                          {currentStatus === "in_transit" && (
                            <button
                              type="button"
                              onClick={() => handleAdvanceStatus(did, "in_transit")}
                              disabled={isUpdatingStatus === did}
                              className="px-2.5 py-1 rounded-sm bg-emerald-50 border border-emerald-300 text-emerald-700 font-semibold hover:bg-emerald-100 transition-colors text-[11px] flex items-center gap-1 cursor-pointer"
                            >
                              <Check className="size-3" />
                              <span>Delivered</span>
                            </button>
                          )}
                          <Link
                            href={`/dispatch/${did}`}
                            className="font-bold text-sky-600 hover:text-sky-800 transition-colors hover:underline"
                          >
                            View
                          </Link>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="pt-2 flex items-center justify-between text-xs font-sans text-gray-500">
          <span>Showing {filteredDispatches.length} of {totalCount} items</span>
        </div>
      </div>

      {/* New Dispatch Modal */}
      <CreateDispatchModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreated={loadData}
      />
    </div>
  );
}
