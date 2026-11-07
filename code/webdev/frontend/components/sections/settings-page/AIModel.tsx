"use client";

import React, { useEffect, useState } from "react";
import { Brain, Check, Cpu, Sparkles, ShieldAlert } from "lucide-react";
import { fetchModelsStatus } from "@/lib/api";

type AIModelProps = {
  confidenceThreshold: number;
  onConfidenceChange: (val: number) => void;
};

const DEFECT_TAXONOMY = [
  { id: "sisik_sisa", label: "0: sisik_sisa", desc: "Scale loss / Parasit Argulus, Anchor worm", color: "bg-amber-50 text-amber-800 border-amber-300" },
  { id: "warna_abnormal", label: "1: warna_abnormal", desc: "Bacterial Red Disease (BRD), Aeromoniasis, Hemorrhage", color: "bg-red-50 text-red-800 border-red-300" },
  { id: "luka_robekan", label: "2: luka_robekan", desc: "Skin ulcer, Fin rot, Saprolegniasis fungal wound", color: "bg-yellow-50 text-yellow-800 border-yellow-300" },
  { id: "lendir_berlebih", label: "3: lendir_berlebih", desc: "White tail disease (WTD), excess clotted mucus", color: "bg-purple-50 text-purple-800 border-purple-300" },
];

export const AIModel = ({
  confidenceThreshold,
  onConfidenceChange,
}: AIModelProps) => {
  const [modelStatus, setModelStatus] = useState<any>(null);

  useEffect(() => {
    let isMounted = true;
    const loadStatus = async () => {
      try {
        const data = await fetchModelsStatus();
        if (isMounted) setModelStatus(data);
      } catch (err) {
        console.warn("Failed to fetch model status:", err);
      }
    };
    loadStatus();
    return () => {
      isMounted = false;
    };
  }, []);

  const freshModel = modelStatus?.freshness_model || modelStatus?.freshnessModel;
  const defectModel = modelStatus?.defect_model || modelStatus?.defectModel;

  const normalizedThreshold =
    confidenceThreshold <= 1.0
      ? Math.round(confidenceThreshold * 100)
      : Math.round(confidenceThreshold);

  return (
    <div className="w-full p-6 bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 flex flex-col gap-6">
      {/* Section Header */}
      <div className="w-full pb-3 border-b border-slate-200 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Brain className="size-5 text-sky-700" />
          <h2 className="text-lg font-bold font-sans text-zinc-900">
            Dual AI Model Inference Architecture
          </h2>
        </div>
        <span className="text-xs font-mono font-bold text-sky-700 bg-sky-50 px-2.5 py-1 rounded-full border border-sky-200">
          ONNX Runtime (CPU)
        </span>
      </div>

      {/* Model Status Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Card 1: Freshness Classifier */}
        <div className="p-4 bg-slate-50 rounded-lg border-l-4 border-emerald-500 border-t border-r border-b border-slate-200 flex flex-col gap-2">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-sm font-bold font-sans text-zinc-900 block">
                Model 1 — Freshness Classifier
              </span>
              <span className="text-xs text-gray-500 font-sans">
                Standar Organoleptik SNI 2729:2013 (Grade A, B, C)
              </span>
            </div>
            <div className="px-2 py-0.5 bg-emerald-100 rounded-sm border border-emerald-300 flex items-center gap-1">
              <div className="size-1.5 bg-emerald-600 rounded-full" />
              <span className="text-[11px] font-bold font-sans text-emerald-800">
                {freshModel?.status || "Loaded (CPU)"}
              </span>
            </div>
          </div>
          <div className="pt-2 border-t border-slate-200 flex justify-between items-center text-xs font-mono text-gray-600">
            <span>MobileNetV3-Small (Float32)</span>
            <span className="font-bold text-zinc-800">Input: [1, 3, 224, 224]</span>
          </div>
        </div>

        {/* Card 2: Defect Detector */}
        <div className="p-4 bg-slate-50 rounded-lg border-l-4 border-rose-500 border-t border-r border-b border-slate-200 flex flex-col gap-2">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-sm font-bold font-sans text-zinc-900 block">
                Model 2 — Surface Defect Detector
              </span>
              <span className="text-xs text-gray-500 font-sans">
                YOLOv8s Real-Time Object Detection (4 Classes)
              </span>
            </div>
            <div className="px-2 py-0.5 bg-emerald-100 rounded-sm border border-emerald-300 flex items-center gap-1">
              <div className="size-1.5 bg-emerald-600 rounded-full" />
              <span className="text-[11px] font-bold font-sans text-emerald-800">
                {defectModel?.status || "Loaded (CPU)"}
              </span>
            </div>
          </div>
          <div className="pt-2 border-t border-slate-200 flex justify-between items-center text-xs font-mono text-gray-600">
            <span>YOLOv8s ONNX (640x640)</span>
            <span className="font-bold text-zinc-800">Input: [1, 3, 640, 640]</span>
          </div>
        </div>
      </div>

      {/* Confidence Threshold Slider */}
      <div className="pt-2 flex flex-col gap-3">
        <div className="flex justify-between items-center">
          <div>
            <span className="text-sm font-bold font-sans text-zinc-900 block">
              Confidence Decision Threshold
            </span>
            <span className="text-xs text-gray-500 font-sans">
              Ambang batas keyakinan model sebelum sistem memicu aktuator reject/conditional.
            </span>
          </div>
          <div className="px-2.5 py-1 bg-rose-50 border border-rose-200 rounded-sm">
            <span className="text-sm font-bold font-mono text-rose-700">
              {normalizedThreshold}%
            </span>
          </div>
        </div>

        {/* Custom Input Range Slider */}
        <div className="relative w-full flex items-center">
          <input
            type="range"
            min="50"
            max="95"
            value={normalizedThreshold}
            onChange={(e) => onConfidenceChange(Number(e.target.value))}
            className="w-full h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer accent-sky-700"
          />
        </div>

        <div className="flex justify-between items-center text-[11px] font-mono text-gray-500">
          <span>50% (Toleran / Deteksi Sensitif)</span>
          <span>95% (Ketat / High Precision)</span>
        </div>
      </div>

      {/* Active Defect Taxonomy (4 Classes) */}
      <div className="pt-4 border-t border-slate-200 flex flex-col gap-3">
        <div>
          <span className="text-sm font-bold font-sans text-zinc-900 block">
            Taksonomi 4 Kelas Cacat Permukaan (YOLOv8s Defects)
          </span>
          <span className="text-xs text-gray-500 font-sans">
            Seluruh kelas telah diselaraskan dengan dataset hasil training di models/model_2.
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {DEFECT_TAXONOMY.map((item) => (
            <div
              key={item.id}
              className={`p-3 rounded-md border ${item.color} flex flex-col gap-1`}
            >
              <span className="text-xs font-bold font-mono">{item.label}</span>
              <span className="text-[11px] font-sans opacity-90">{item.desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
