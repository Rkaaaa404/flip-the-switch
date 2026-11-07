"use client";

import React from "react";
import { RecentInspections } from "./RecentInspections";
import { HardwareStatus } from "./HardwareStatus";
import { LotRecord, HardwareStatus as HardwareStatusType } from "@/types";

interface BodySectionProps {
  lots?: LotRecord[] | null;
  hardwareStatus?: HardwareStatusType | null;
  isLoading?: boolean;
}

export const BodySection = ({ lots, hardwareStatus, isLoading = false }: BodySectionProps) => {
  return (
    <div className="flex flex-col lg:flex-row gap-6 min-h-[460px]">
      <RecentInspections lots={lots} isLoading={isLoading} />
      <HardwareStatus status={hardwareStatus} isLoading={isLoading} />
    </div>
  );
};
