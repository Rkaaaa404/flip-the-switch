"use client";

import { useEffect, useState, useCallback } from "react";
import { HeadSection } from "@/components/sections/dashboard-page/HeadSection";
import { BodySection } from "@/components/sections/dashboard-page/BodySection";
import { fetchDashboardStats, fetchRecentLots, fetchHardwareStatus } from "@/lib/api";
import { DashboardStats, LotRecord, HardwareStatus as HardwareStatusType } from "@/types";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentLots, setRecentLots] = useState<LotRecord[]>([]);
  const [hardware, setHardware] = useState<HardwareStatusType | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [lastRefreshed, setLastRefreshed] = useState<Date>(new Date());

  const loadAllData = useCallback(async (showLoader = false) => {
    if (showLoader) setIsLoading(true);
    try {
      const [sData, lData, hData] = await Promise.all([
        fetchDashboardStats().catch(() => null),
        fetchRecentLots(5).catch(() => []),
        fetchHardwareStatus().catch(() => null),
      ]);
      if (sData) setStats(sData);
      if (lData) setRecentLots(lData);
      if (hData) setHardware(hData);
      setLastRefreshed(new Date());
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial load + periodic polling fallback
  useEffect(() => {
    loadAllData(true);
    const interval = setInterval(() => {
      loadAllData(false);
    }, 10000); // 10s auto-refresh
    return () => clearInterval(interval);
  }, [loadAllData]);

  // WebSocket Live Real-time Connection
  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/events";
    let ws: WebSocket | null = null;
    let reconnectTimeout: NodeJS.Timeout;

    const connectWebSocket = () => {
      try {
        ws = new WebSocket(wsUrl);
        ws.onopen = () => {
          setWsConnected(true);
        };
        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (data.type === "NEW_INSPECTION" || data.event === "NEW_INSPECTION") {
              // Immediately refresh data on new inspection
              loadAllData(false);
            }
          } catch {
            // Non-json ping/pong
          }
        };
        ws.onerror = () => {
          setWsConnected(false);
        };
        ws.onclose = () => {
          setWsConnected(false);
          reconnectTimeout = setTimeout(connectWebSocket, 5000);
        };
      } catch {
        setWsConnected(false);
      }
    };

    connectWebSocket();

    return () => {
      if (ws) ws.close();
      clearTimeout(reconnectTimeout);
    };
  }, [loadAllData]);

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      {/* KPI Stat Cards */}
      <HeadSection stats={stats} isLoading={isLoading} />

      {/* Live Table + Hardware Card */}
      <BodySection lots={recentLots} hardwareStatus={hardware} isLoading={isLoading} />
    </div>
  );
}