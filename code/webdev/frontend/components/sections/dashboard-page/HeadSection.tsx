"use client";

import React, { useEffect, useState } from "react";
import { StatCard } from "@/components/common/StatCard";
import {
  CheckCircle2,
  AlertTriangle,
  Cpu,
  BriefcaseConveyorBelt,
  Loader2,
} from "lucide-react";
import { fetchDashboardStats } from "@/lib/api";
import { DashboardStats } from "@/types";

interface HeadSectionProps {
  stats?: DashboardStats | null;
  isLoading?: boolean;
}

export function HeadSection({ stats: propStats, isLoading = false }: HeadSectionProps) {
  const [internalStats, setInternalStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (propStats !== undefined) return;

    let isMounted = true;
    const loadStats = async () => {
      try {
        setLoading(true);
        const data = await fetchDashboardStats();
        if (isMounted) setInternalStats(data);
      } catch (err) {
        console.warn("Failed to fetch dashboard stats:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadStats();
    return () => {
      isMounted = false;
    };
  }, [propStats]);

  const activeStats = propStats !== undefined ? propStats : internalStats;
  const isFetching = isLoading || (loading && !activeStats);

  const totalInspected = activeStats
    ? (activeStats.total_inspected_today ?? activeStats.totalInspectedToday ?? 0).toLocaleString()
    : "0";

  const currentLot = activeStats?.current_lot_id || activeStats?.currentLotId || "LOT-READY";
  const passRate = activeStats ? (activeStats.pass_rate ?? activeStats.passRate ?? 100.0).toFixed(1) : "100.0";
  const failRate = activeStats ? (activeStats.fail_rate ?? activeStats.failRate ?? 0.0).toFixed(1) : "0.0";
  const avgConf = activeStats ? (activeStats.avg_confidence ?? activeStats.avg_confidence_score ?? 95.0).toFixed(1) : "95.0";

  const passDelta = activeStats?.pass_rate_delta ?? activeStats?.passRateDelta ?? 0.0;
  const failDelta = activeStats?.fail_rate_delta ?? activeStats?.failRateDelta ?? 0.0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Total Inspected */}
      <StatCard
        title="Total Inspected Today"
        value={isFetching ? "..." : totalInspected}
        unit="ikan"
        subtext={`Lot Aktif: ${currentLot}`}
        icon={<BriefcaseConveyorBelt className="size-5 text-sky-700" />}
      />

      {/* 2. Pass Rate */}
      <StatCard
        title="Pass Rate (Lolos)"
        value={isFetching ? "..." : `${passRate}%`}
        delta={passDelta !== 0 ? `${passDelta > 0 ? "+" : ""}${passDelta}%` : undefined}
        deltaPositive={passDelta >= 0}
        valueColor="text-green-600"
        icon={<CheckCircle2 className="size-5 text-green-600" />}
      />

      {/* 3. Fail Rate */}
      <StatCard
        title="Fail Rate (Reject)"
        value={isFetching ? "..." : `${failRate}%`}
        delta={failDelta !== 0 ? `${failDelta > 0 ? "+" : ""}${failDelta}%` : undefined}
        deltaPositive={failDelta <= 0}
        valueColor="text-red-500"
        icon={<AlertTriangle className="size-5 text-red-500" />}
      />

      {/* 4. Avg Confidence */}
      <StatCard
        title="Avg Confidence Score"
        value={isFetching ? "..." : `${avgConf}%`}
        valueColor="text-sky-600"
        subtext="Dual ONNX Inference"
        icon={<Cpu className="size-5 text-sky-500" />}
      />
    </div>
  );
}
