"use client";

import React from "react";
import { Check, X, AlertTriangle, Clock, ShieldCheck, Sparkles, Inbox } from "lucide-react";
import { TowerLight } from "@/components/common/TowerLight";
import { InspectionResult } from "@/types";

interface ResultSectionProps {
  result?: InspectionResult | null;
  isLoading?: boolean;
}

const decisionConfig: Record<string, { bg: string; text: string; border: string; label: string; icon: React.ReactNode }> = {
  PASS: {
    bg: "bg-green-50",
    text: "text-green-700",
    border: "border-green-300",
    label: "PASS (Lolos Mutu)",
    icon: <Check className="size-6 text-green-700 stroke-[3]" />,
  },
  CONDITIONAL: {
    bg: "bg-amber-50",
    text: "text-amber-700",
    border: "border-amber-300",
    label: "CONDITIONAL (Verifikasi Operator)",
    icon: <AlertTriangle className="size-6 text-amber-700 stroke-[2.5]" />,
  },
  FAIL: {
    bg: "bg-red-50",
    text: "text-red-700",
    border: "border-red-300",
    label: "FAIL (Reject / Tolak)",
    icon: <X className="size-6 text-red-700 stroke-[3]" />,
  },
};

const gradeColorMap: Record<string, { bg: string; text: string; border: string; ring: string; progress: string; desc: string }> = {
  A: {
    bg: "bg-green-50",
    text: "text-green-700",
    border: "border-green-500",
    ring: "outline-green-500/30",
    progress: "bg-green-600",
    desc: "Kualitas Prima — Standar Ekspor (SNI 2729:2013)",
  },
  B: {
    bg: "bg-amber-50",
    text: "text-amber-700",
    border: "border-amber-500",
    ring: "outline-amber-500/30",
    progress: "bg-amber-500",
    desc: "Kualitas Baik — Standar Konsumsi Pasar Domestik",
  },
  C: {
    bg: "bg-red-50",
    text: "text-red-700",
    border: "border-red-500",
    ring: "outline-red-500/30",
    progress: "bg-red-600",
    desc: "Kualitas Rendah / Busuk — Rekomendasi Reject",
  },
};

const defectBadgeStyles: Record<string, { bg: string; text: string; border: string }> = {
  sisik_sisa: { bg: "bg-amber-50", text: "text-amber-800", border: "border-amber-300" },
  warna_abnormal: { bg: "bg-red-50", text: "text-red-800", border: "border-red-300" },
  luka_robekan: { bg: "bg-yellow-50", text: "text-yellow-800", border: "border-yellow-300" },
  lendir_berlebih: { bg: "bg-purple-50", text: "text-purple-800", border: "border-purple-300" },
};

export const ResultSection = ({ result, isLoading = false }: ResultSectionProps) => {
  // Empty state when no inspection has run yet
  if (!result && !isLoading) {
    return (
      <div className="w-full h-full min-h-[460px] bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 p-8 flex flex-col items-center justify-center text-center gap-4">
        <div className="size-16 rounded-full bg-slate-100 flex items-center justify-center text-slate-400">
          <Inbox className="size-8 stroke-[1.5]" />
        </div>
        <div className="max-w-xs">
          <h3 className="text-base font-bold font-sans text-zinc-900">Menunggu Sampel Inspeksi</h3>
          <p className="text-xs font-sans text-gray-500 mt-1">
            Unggah citra ikan atau pilih sampel demo di panel sebelah kiri, lalu klik &quot;Jalankan Inspeksi AI&quot;.
          </p>
        </div>
      </div>
    );
  }

  // Loading skeleton state
  if (isLoading || !result) {
    return (
      <div className="w-full h-full min-h-[460px] bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 p-8 flex flex-col items-center justify-center text-center gap-4 animate-pulse">
        <div className="size-14 rounded-full bg-sky-100 flex items-center justify-center text-sky-500">
          <Sparkles className="size-7 animate-spin" />
        </div>
        <p className="text-sm font-bold font-sans text-sky-800">Sedang Menganalisis Citra Ikan...</p>
        <p className="text-xs font-mono text-gray-400">Menghitung matriks kesegaran & lokalisasi cacat visual</p>
      </div>
    );
  }

  const decisionKey = result.decision || "PASS";
  const decisionStyle = decisionConfig[decisionKey] || decisionConfig.PASS;
  const gradeKey = result.grade || "A";
  const gradeStyle = gradeColorMap[gradeKey] || gradeColorMap.A;
  const confidenceVal = Math.round(
    result.confidence !== undefined
      ? result.confidence > 1.0 ? result.confidence : result.confidence * 100
      : (result.grade_confidence ? result.grade_confidence * 100 : 90)
  );

  const signal = result.conveyorSignal || result.hardware_signal || (result.decision === "FAIL" ? "RED" : "GREEN");

  return (
    <div className="w-full flex flex-col gap-4">
      {/* 1. Decision Banner (PASS / CONDITIONAL / FAIL) */}
      <div
        className={`w-full px-6 py-4 ${decisionStyle.bg} rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] border ${decisionStyle.border} flex flex-col justify-center items-center gap-1`}
      >
        <div className="flex items-center gap-2">
          {decisionStyle.icon}
          <span className={`text-2xl font-black font-sans tracking-wide leading-none ${decisionStyle.text}`}>
            {decisionStyle.label}
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono font-medium text-gray-600 mt-1">
          <span className="font-semibold text-zinc-900">{result.lotId || result.lot_id}</span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <Clock className="size-3 text-gray-400" />
            {result.processingTimeMs || result.processing_time_ms || 120}ms
          </span>
        </div>
      </div>

      {/* 2. Freshness Grade Card */}
      <div
        className={`w-full p-6 bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] border-l-4 ${gradeStyle.border} border-t border-r border-b border-slate-200 flex flex-col gap-4`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="size-5 text-sky-700" />
            <h3 className="text-lg font-bold font-sans text-zinc-900">Freshness Grade (Model 1)</h3>
          </div>
          <span className="text-xs font-mono font-semibold text-sky-700 bg-sky-50 px-2 py-0.5 rounded-sm border border-sky-200">
            SNI 2729:2013
          </span>
        </div>

        <div className="flex items-center gap-5">
          {/* Grade Badge Circle */}
          <div
            className={`size-16 shrink-0 ${gradeStyle.bg} rounded-full outline outline-2 outline-offset-[-2px] ${gradeStyle.ring} flex flex-col justify-center items-center shadow-xs`}
          >
            <span className={`text-3xl font-black font-sans leading-none ${gradeStyle.text}`}>
              {result.grade}
            </span>
          </div>

          {/* Confidence & Note */}
          <div className="flex-1 flex flex-col gap-1.5 min-w-0">
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-zinc-600 font-medium">Confidence Score</span>
              <span className="text-zinc-900 font-bold">{confidenceVal}%</span>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-2.5 bg-zinc-100 rounded-full overflow-hidden border border-slate-200">
              <div
                className={`h-full ${gradeStyle.progress} rounded-full transition-all duration-700`}
                style={{ width: `${confidenceVal}%` }}
              />
            </div>

            {/* Note */}
            <p className="pt-0.5 text-xs text-gray-600 font-sans">
              {gradeStyle.desc}
            </p>
          </div>
        </div>
      </div>

      {/* 3. Defect Detection Card */}
      <div className="w-full p-6 bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] border-l-4 border-rose-500 border-t border-r border-b border-slate-200 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold font-sans text-zinc-900">
            Defect Detection (Model 2 YOLOv8s)
          </h3>
          <span className="text-xs font-mono font-semibold px-2 py-0.5 bg-slate-100 rounded-sm text-gray-700">
            {result.defects?.length || 0} Cacat Terdeteksi
          </span>
        </div>

        {/* Defect tags */}
        <div className="flex flex-wrap gap-2 pt-1">
          {result.defects && result.defects.length > 0 ? (
            result.defects.map((defect, index) => {
              const bStyle = defectBadgeStyles[defect.label] || {
                bg: "bg-red-50",
                text: "text-red-800",
                border: "border-red-300",
              };
              const defConf = Math.round(
                defect.confidence > 1.0 ? defect.confidence : defect.confidence * 100
              );

              return (
                <div
                  key={`${defect.label}-${index}`}
                  className={`px-3 py-1.5 rounded-md border ${bStyle.border} ${bStyle.bg} flex items-center gap-1.5 text-xs font-mono ${bStyle.text}`}
                >
                  <span className="font-bold">{defect.label}</span>
                  <span className="opacity-75 font-semibold">({defConf}%)</span>
                </div>
              );
            })
          ) : (
            <div className="p-3 w-full bg-emerald-50 border border-emerald-200 rounded-md text-xs font-sans text-emerald-800 flex items-center gap-2">
              <Check className="size-4 text-emerald-600" />
              <span>Tidak ada cacat atau penyakit permukaan yang terdeteksi (Permukaan Bersih).</span>
            </div>
          )}
        </div>
      </div>

      {/* 4. Conveyor Signal Card */}
      <div className="w-full p-5 bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 flex items-center justify-between gap-4">
        <div className="flex flex-col gap-0.5">
          <span className="text-xs font-bold font-sans uppercase tracking-wider text-gray-500">
            Hardware Conveyor Actuator
          </span>
          <span className="text-sm font-bold font-sans text-zinc-900">
            {signal === "GREEN" && "Conveyor Running (Lolos Sortir)"}
            {signal === "YELLOW" && "Conveyor Slow (Pemeriksaan Manual)"}
            {signal === "RED" && "Conveyor Reject / Ejector Aktif"}
          </span>
        </div>
        <TowerLight signal={signal as "GREEN" | "YELLOW" | "RED"} />
      </div>
    </div>
  );
};
