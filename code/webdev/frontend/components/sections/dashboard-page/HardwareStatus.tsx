"use client";

import React, { useEffect, useState } from "react";
import { Server, RefreshCw, Radio, Check, AlertCircle } from "lucide-react";
import { HardwareBadge } from "@/components/common/HardwareBadge";
import { TowerLight } from "@/components/common/TowerLight";
import { Switch } from "@/components/ui/Switch";
import { fetchHardwareStatus, saveSettings } from "@/lib/api";
import { HardwareStatus as HardwareStatusType } from "@/types";

interface HardwareStatusProps {
  status?: HardwareStatusType | null;
  isLoading?: boolean;
}

export const HardwareStatus = ({ status: propStatus, isLoading = false }: HardwareStatusProps) => {
  const [internalStatus, setInternalStatus] = useState<HardwareStatusType | null>(null);
  const [mockEnabled, setMockEnabled] = useState<boolean>(true);
  const [isUpdating, setIsUpdating] = useState<boolean>(false);

  useEffect(() => {
    if (propStatus !== undefined && propStatus !== null) {
      setMockEnabled(Boolean(propStatus.mock_mode ?? propStatus.mockMode ?? propStatus.mockModeEnabled ?? true));
      return;
    }

    let isMounted = true;
    const loadHardware = async () => {
      try {
        const data = await fetchHardwareStatus();
        if (isMounted) {
          setInternalStatus(data);
          setMockEnabled(Boolean(data.mock_mode ?? data.mockMode ?? data.mockModeEnabled ?? true));
        }
      } catch (err) {
        console.warn("Failed to fetch hardware status:", err);
      }
    };

    loadHardware();
    return () => {
      isMounted = false;
    };
  }, [propStatus]);

  const activeStatus = propStatus !== undefined && propStatus !== null ? propStatus : internalStatus;

  const handleToggleMock = async (checked: boolean) => {
    setMockEnabled(checked);
    setIsUpdating(true);
    try {
      await saveSettings({ mock_mode_enabled: checked, mockModeEnabled: checked });
    } catch (err) {
      console.warn("Failed to update mock mode setting:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const cameraState = activeStatus?.camera || "ONLINE";
  const conveyorState = activeStatus?.conveyor_relay || activeStatus?.conveyor || "ACTIVE";
  const towerSignal = activeStatus?.tower_light || activeStatus?.towerLight || "GREEN";

  return (
    <div className="w-full lg:w-80 self-stretch p-6 bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-offset-[-1px] outline-slate-300 flex flex-col gap-4 overflow-hidden">
      {/* Header */}
      <div className="pb-3 border-b border-slate-200 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Server className="size-4 text-sky-700" />
          <span className="text-base font-bold font-sans text-zinc-900">Hardware Peripheral</span>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-green-50 text-green-700 border border-green-200 rounded-full">
          Raspberry Pi 5
        </span>
      </div>

      {/* Status Rows */}
      <div className="flex-1 flex flex-col gap-3.5">
        <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-md border border-slate-100">
          <span className="text-sm font-semibold font-sans text-gray-700">Snapshot Camera</span>
          <HardwareBadge status={cameraState} />
        </div>

        <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-md border border-slate-100">
          <span className="text-sm font-semibold font-sans text-gray-700">Conveyor Relay (GPIO)</span>
          <HardwareBadge status={conveyorState} />
        </div>

        <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-md border border-slate-100">
          <span className="text-sm font-semibold font-sans text-gray-700">Tower Light Actuator</span>
          <TowerLight signal={towerSignal} />
        </div>
      </div>

      {/* Footer — Mock Toggle */}
      <div className="pt-3 border-t border-slate-200 flex flex-col gap-1.5">
        <div className="flex justify-between items-center">
          <div className="flex flex-col">
            <span className="text-xs font-bold font-mono text-zinc-800">ENABLE_MOCK_HARDWARE</span>
            <span className="text-[11px] font-sans text-gray-500">
              {mockEnabled ? "Simulasi GPIO lokal aktif" : "Mode Pin GPIO Fisik"}
            </span>
          </div>
          <Switch
            checked={mockEnabled}
            onCheckedChange={handleToggleMock}
            disabled={isUpdating}
            id="mock-hardware-toggle"
          />
        </div>
      </div>
    </div>
  );
};
