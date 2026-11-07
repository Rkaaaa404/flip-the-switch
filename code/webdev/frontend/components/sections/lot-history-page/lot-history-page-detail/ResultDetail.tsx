"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Download,
  Info,
  Clock,
  Radio,
  AlertTriangle,
  X,
  Check,
  Loader2,
  Inbox,
  ShieldCheck,
  Sparkles,
  ArrowLeft,
  RotateCcw,
  Edit3,
  FileText,
  CheckCircle2,
  Cpu,
  Save,
  AlertCircle,
} from "lucide-react";
import { fetchLotById, updateLotNote, overrideLotDecision } from "@/lib/api";
import { LotRecord, Defect } from "@/types";

const DEFECT_COLOR_MAP: Record<string, { border: string; bg: string; text: string; label: string; bar: string }> = {
  sisik_sisa: { border: "border-red-600", bg: "bg-red-600", text: "text-white", label: "sisik_sisa", bar: "bg-red-600" },
  mata_keruh: { border: "border-amber-500", bg: "bg-amber-600", text: "text-white", label: "mata_keruh", bar: "bg-amber-500" },
  warna_abnormal: { border: "border-red-600", bg: "bg-red-600", text: "text-white", label: "warna_abnormal", bar: "bg-red-600" },
  luka_robekan: { border: "border-yellow-500", bg: "bg-yellow-600", text: "text-white", label: "luka_robekan", bar: "bg-yellow-500" },
  lendir_berlebih: { border: "border-purple-600", bg: "bg-purple-600", text: "text-white", label: "lendir_berlebih", bar: "bg-purple-600" },
};

type ResultDetailProps = {
  lotId: string;
};

export const ResultDetail = ({ lotId }: ResultDetailProps) => {
  const router = useRouter();
  const [lot, setLot] = useState<LotRecord | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [imageDimensions, setImageDimensions] = useState<{ naturalWidth: number; naturalHeight: number } | null>(null);

  // Inspector Note state
  const [inspectorNote, setInspectorNote] = useState<string>("");
  const [isSavingNote, setIsSavingNote] = useState<boolean>(false);
  const [noteSavedToast, setNoteSavedToast] = useState<boolean>(false);

  // Override Modal state
  const [isOverrideModalOpen, setIsOverrideModalOpen] = useState<boolean>(false);
  const [overrideDecisionVal, setOverrideDecisionVal] = useState<"PASS" | "FAIL" | "CONDITIONAL">("PASS");
  const [overrideReason, setOverrideReason] = useState<string>("Manual supervisor verification & visual confirmation");
  const [isOverriding, setIsOverriding] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;
    const loadDetail = async () => {
      setIsLoading(true);
      try {
        const data = await fetchLotById(lotId);
        if (isMounted && data) {
          setLot(data);
          const initialNote = data.inspector_note || data.inspectorNote || "";
          setInspectorNote(initialNote);
        }
      } catch (err) {
        console.warn("Failed to fetch lot details:", err);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };

    loadDetail();
    return () => {
      isMounted = false;
    };
  }, [lotId]);

  const handleImageLoaded = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    setImageDimensions({
      naturalWidth: img.naturalWidth || 640,
      naturalHeight: img.naturalHeight || 480,
    });
  };

  const handleSaveNote = async () => {
    if (!lot) return;
    setIsSavingNote(true);
    try {
      await updateLotNote(lot.lotId || lot.lot_id || lotId, inspectorNote);
      setNoteSavedToast(true);
      setTimeout(() => setNoteSavedToast(false), 3000);
    } catch (err) {
      console.warn("Failed to save note:", err);
    } finally {
      setIsSavingNote(false);
    }
  };

  const handleApplyOverride = async () => {
    if (!lot) return;
    setIsOverriding(true);
    try {
      const res = await overrideLotDecision(
        lot.lotId || lot.lot_id || lotId,
        overrideDecisionVal,
        overrideReason
      );
      setLot((prev) =>
        prev
          ? {
              ...prev,
              decision: overrideDecisionVal,
              hardware_signal: (res.hardware_signal as any) || (overrideDecisionVal === "PASS" ? "GREEN" : overrideDecisionVal === "CONDITIONAL" ? "YELLOW" : "RED"),
              conveyorSignal: (res.hardware_signal as any) || (overrideDecisionVal === "PASS" ? "GREEN" : overrideDecisionVal === "CONDITIONAL" ? "YELLOW" : "RED"),
            }
          : prev
      );
      setIsOverrideModalOpen(false);
    } catch (err) {
      console.warn("Failed to override decision:", err);
    } finally {
      setIsOverriding(false);
    }
  };

  if (isLoading) {
    return (
      <div className="w-full bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-16 flex flex-col items-center justify-center gap-3">
        <Loader2 className="size-8 animate-spin text-sky-600" />
        <p className="text-sm font-semibold font-sans text-zinc-800">Memuat Detail Lot {lotId}...</p>
      </div>
    );
  }

  if (!lot) {
    return (
      <div className="w-full bg-white rounded-lg shadow-xs outline outline-1 outline-slate-300 p-16 flex flex-col items-center justify-center gap-4 text-center">
        <Inbox className="size-10 text-slate-300" />
        <div>
          <h2 className="text-lg font-bold font-sans text-zinc-900">Catatan Lot Tidak Ditemukan</h2>
          <p className="text-xs font-sans text-gray-500 mt-1">
            Lot ID &quot;{lotId}&quot; tidak tersimpan di database audit inspeksi.
          </p>
        </div>
        <Link
          href="/history"
          className="inline-flex items-center gap-2 px-4 py-2 bg-sky-700 text-white text-xs font-bold font-sans rounded-sm hover:bg-sky-800 transition-colors"
        >
          <ArrowLeft className="size-3.5" />
          <span>Kembali ke Daftar Riwayat</span>
        </Link>
      </div>
    );
  }

  const decision = (lot.decision || "PASS").toUpperCase();
  const isPass = decision === "PASS";
  const isConditional = decision === "CONDITIONAL";
  const isFail = decision === "FAIL";

  const gradeKey = lot.grade || "A";
  const confidenceVal =
    lot.confidence !== undefined
      ? lot.confidence > 1.0 ? Number(lot.confidence.toFixed(1)) : Number((lot.confidence * 100).toFixed(1))
      : (lot.grade_confidence ? Number((lot.grade_confidence * 100).toFixed(1)) : 90.0);

  const rawSignal = lot.conveyorSignal || lot.hardware_signal || (isFail ? "RED" : isConditional ? "YELLOW" : "GREEN");
  const defectsList: Defect[] = lot.defects || [];

  // Parse formatted date and time
  let formattedDate = "2026-08-22";
  let formattedTime = "10:24:50";
  try {
    const d = new Date(lot.timestamp);
    if (!isNaN(d.getTime())) {
      formattedDate = d.toISOString().split("T")[0];
      formattedTime = d.toTimeString().split(" ")[0];
    }
  } catch {
    // fallback
  }

  // Construct absolute image URL
  const backendBase = process.env.NEXT_PUBLIC_API_URL?.replace("/api/v1", "") || "http://localhost:8000";
  const imgSrc = lot.imageUrl
    ? lot.imageUrl.startsWith("http") ? lot.imageUrl : `${backendBase}${lot.imageUrl}`
    : lot.image_path
    ? lot.image_path.startsWith("http") ? lot.image_path : `${backendBase}${lot.image_path}`
    : "";

  // Organoleptic breakdown indicators
  const eyeClarity = gradeKey === "A" ? { text: "Good", color: "text-emerald-600 bg-emerald-500" } : gradeKey === "B" ? { text: "Fair", color: "text-amber-600 bg-amber-500" } : { text: "Poor", color: "text-rose-600 bg-rose-500" };
  const scaleCondition = defectsList.length === 0 ? { text: "Good", color: "text-emerald-600 bg-emerald-500" } : defectsList.length <= 2 ? { text: "Fair", color: "text-amber-600 bg-amber-500" } : { text: "Poor", color: "text-rose-600 bg-rose-500" };

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Header section with back button */}
      <div className="flex flex-col gap-1">
        <Link
          href="/history"
          className="inline-flex items-center gap-1 text-xs font-bold font-sans text-sky-600 hover:text-sky-800 transition-colors w-fit"
        >
          <ArrowLeft className="size-3.5" />
          <span>Back to Lot History</span>
        </Link>
        <h1 className="text-xl font-bold font-sans text-zinc-900">Inspection Detail</h1>
        <p className="text-xs font-mono font-semibold text-gray-500">{lot.lotId || lot.lot_id || lotId}</p>
      </div>

      {/* Main 2-Column Grid */}
      <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN: Image Scan with Bounding Boxes (col-span-6 or 7) */}
        <div className="lg:col-span-6 w-full bg-white rounded-lg shadow-xs border border-slate-200 flex flex-col overflow-hidden">
          <div className="relative bg-slate-900 flex justify-center items-center min-h-[380px] max-h-[460px] overflow-hidden">
            {imgSrc ? (
              <div className="relative w-full h-full flex items-center justify-center">
                <img
                  src={imgSrc}
                  alt={`Scan of ${lotId}`}
                  onLoad={handleImageLoaded}
                  className="w-full h-full max-h-[440px] object-contain"
                />

                {/* YOLOv8 Defect Bounding Boxes */}
                {defectsList.length > 0 && imageDimensions && (
                  <div className="absolute inset-0 pointer-events-none">
                    {defectsList.map((defect, idx) => {
                      const [x1, y1, x2, y2] = defect.bbox || [0, 0, 0, 0];
                      const nw = imageDimensions.naturalWidth || 640;
                      const nh = imageDimensions.naturalHeight || 480;

                      const leftPct = (x1 / nw) * 100;
                      const topPct = (y1 / nh) * 100;
                      const widthPct = Math.max(3, ((x2 - x1) / nw) * 100);
                      const heightPct = Math.max(3, ((y2 - y1) / nh) * 100);

                      const styleInfo = DEFECT_COLOR_MAP[defect.label] || {
                        border: "border-red-600",
                        bg: "bg-red-600",
                        text: "text-white",
                        label: defect.label,
                      };

                      const defConf = Math.round(
                        defect.confidence > 1.0 ? defect.confidence : defect.confidence * 100
                      );

                      return (
                        <div
                          key={`${defect.label}-${idx}`}
                          className={`absolute border-2 ${styleInfo.border} rounded-xs`}
                          style={{
                            left: `${leftPct}%`,
                            top: `${topPct}%`,
                            width: `${widthPct}%`,
                            height: `${heightPct}%`,
                          }}
                        >
                          <span
                            className={`absolute -top-5 left-0 px-1.5 py-0.5 text-[10px] font-mono font-bold ${styleInfo.bg} ${styleInfo.text} rounded-xs shadow-sm whitespace-nowrap`}
                          >
                            {styleInfo.label} {defConf}%
                          </span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center gap-2 text-slate-400 p-12">
                <Inbox className="size-10" />
                <span className="text-xs font-mono">Snapshot citra tidak tersedia</span>
              </div>
            )}
          </div>

          {/* Dark Footer bar with Latency and Model info */}
          <div className="px-4 py-3 bg-zinc-900 flex justify-between items-center text-xs font-mono text-gray-300 border-t border-zinc-800">
            <div className="flex items-center gap-2">
              <Cpu className="size-3.5 text-sky-400" />
              <span>Processed in {lot.processingTimeMs || lot.processing_time_ms || 245}ms</span>
            </div>
            <div className="text-slate-400 text-[11px]">
              Model: YOLOv8s-defect + MobileNetV3-freshness
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Metadata, Analysis, Hardware Log, Actions (col-span-6) */}
        <div className="lg:col-span-6 w-full flex flex-col gap-4">
          {/* 1. Large Decision Pill Badge (Top Right) */}
          <div className="w-full flex justify-end">
            <div
              className={`px-8 py-2.5 rounded-full flex items-center justify-center gap-2 text-xl font-black font-sans tracking-wide shadow-xs ${
                isPass
                  ? "bg-emerald-50 text-emerald-600 border border-emerald-200"
                  : isConditional
                  ? "bg-amber-50 text-amber-700 border border-amber-200"
                  : "bg-red-50 text-red-600 border border-red-200"
              }`}
            >
              {isPass && <Check className="size-5 stroke-[3]" />}
              {isConditional && <AlertTriangle className="size-5 stroke-[2.5]" />}
              {isFail && <X className="size-5 stroke-[3]" />}
              <span>{decision}</span>
            </div>
          </div>

          {/* 2. Metadata & Inspector Note Card */}
          <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col gap-3">
            <div className="grid grid-cols-2 gap-4 pb-3 border-b border-slate-100 text-xs font-sans">
              <div>
                <span className="font-semibold text-gray-400 block text-[11px]">Timestamp</span>
                <span className="font-medium text-zinc-900 mt-0.5 block">
                  Inspected at <strong className="font-mono">{formattedTime}</strong> on <strong className="font-mono">{formattedDate}</strong>
                </span>
              </div>
              <div>
                <span className="font-semibold text-gray-400 block text-[11px]">Subject</span>
                <span className="font-medium text-zinc-900 mt-0.5 block">
                  Family: <strong>{lot.fishFamily || lot.fish_family || lot.family || "Scombridae"}</strong>
                </span>
              </div>
            </div>

            {/* Inspector Note Section */}
            <div className="flex flex-col gap-1.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-xs font-bold text-gray-700 font-sans">
                  <FileText className="size-3.5 text-gray-500" />
                  <span>Inspector Note</span>
                </div>
                {noteSavedToast && (
                  <span className="text-[10px] font-sans font-bold text-emerald-600 flex items-center gap-1">
                    <CheckCircle2 className="size-3" /> Tersimpan
                  </span>
                )}
              </div>

              <div className="flex gap-2">
                <input
                  type="text"
                  value={inspectorNote}
                  onChange={(e) => setInspectorNote(e.target.value)}
                  onBlur={handleSaveNote}
                  placeholder='Catatan supervisor (misal: "Batch dari cold storage lot #C-22")'
                  className="flex-1 bg-slate-50 border border-slate-200 rounded-sm px-3 py-2 text-xs font-sans text-zinc-800 focus:bg-white focus:outline-sky-600 transition-colors"
                />
                <button
                  type="button"
                  onClick={handleSaveNote}
                  disabled={isSavingNote}
                  className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-zinc-700 border border-slate-300 rounded-sm text-xs font-bold font-sans transition-colors cursor-pointer flex items-center gap-1"
                  title="Simpan Catatan"
                >
                  {isSavingNote ? <Loader2 className="size-3.5 animate-spin" /> : <Save className="size-3.5" />}
                  <span>Save</span>
                </button>
              </div>
            </div>
          </div>

          {/* 3. Side-by-Side Analysis Cards (Freshness & Detected Defects) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Freshness Analysis Card */}
            <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col justify-between gap-3">
              <h3 className="text-sm font-bold font-sans text-zinc-900">Freshness Analysis</h3>

              <div className="flex items-center gap-3">
                <div
                  className={`size-12 shrink-0 rounded-full flex items-center justify-center font-black text-xl font-sans ${
                    gradeKey === "A"
                      ? "bg-emerald-100 text-emerald-700"
                      : gradeKey === "B"
                      ? "bg-amber-100 text-amber-700"
                      : "bg-red-100 text-red-600"
                  }`}
                >
                  {gradeKey}
                </div>
                <div className="flex-1 flex flex-col gap-1">
                  <div className="flex justify-between items-center text-xs font-sans">
                    <span className="text-gray-500 text-[11px]">Overall Confidence</span>
                    <span className="font-mono font-bold text-zinc-900">{confidenceVal}%</span>
                  </div>
                  <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                    <div
                      className={`h-full rounded-full ${
                        gradeKey === "A" ? "bg-emerald-600" : gradeKey === "B" ? "bg-amber-500" : "bg-red-600"
                      }`}
                      style={{ width: `${confidenceVal}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Organoleptic sub-indicators */}
              <div className="pt-2 border-t border-slate-100 flex flex-col gap-1 text-xs font-sans">
                <div className="flex justify-between items-center text-gray-600">
                  <span>Eye clarity</span>
                  <span className="flex items-center gap-1.5 font-semibold text-zinc-800">
                    <span className={`size-2 rounded-full ${eyeClarity.color.split(" ")[1]}`} />
                    {eyeClarity.text}
                  </span>
                </div>
                <div className="flex justify-between items-center text-gray-600">
                  <span>Scale condition</span>
                  <span className="flex items-center gap-1.5 font-semibold text-zinc-800">
                    <span className={`size-2 rounded-full ${scaleCondition.color.split(" ")[1]}`} />
                    {scaleCondition.text}
                  </span>
                </div>
              </div>
            </div>

            {/* Detected Defects Card */}
            <div className="p-4 bg-white rounded-lg border border-slate-200 shadow-xs flex flex-col justify-between gap-3">
              <h3 className="text-sm font-bold font-sans text-zinc-900">
                Detected Defects ({defectsList.length})
              </h3>

              <div className="flex flex-col gap-2.5 flex-1 justify-center">
                {defectsList.length > 0 ? (
                  defectsList.map((defect, idx) => {
                    const defConf = Math.round(
                      defect.confidence > 1.0 ? defect.confidence : defect.confidence * 100
                    );
                    const isRed = defConf > 75 || defect.label === "sisik_sisa";

                    return (
                      <div key={`${defect.label}-${idx}`} className="flex flex-col gap-1">
                        <div className="flex items-center justify-between text-xs font-sans">
                          <div className="flex items-center gap-1.5 font-mono font-bold text-zinc-900">
                            <AlertTriangle className={`size-3.5 ${isRed ? "text-rose-600" : "text-amber-500"}`} />
                            <span>{defect.label}</span>
                          </div>
                          <span className="font-mono text-xs font-bold text-gray-700">{defConf}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                          <div
                            className={`h-full rounded-full ${isRed ? "bg-red-600" : "bg-amber-500"}`}
                            style={{ width: `${defConf}%` }}
                          />
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-md text-xs font-sans text-emerald-800 flex items-center gap-2">
                    <Check className="size-4 text-emerald-600 shrink-0" />
                    <span>Tidak ada cacat permukaan terdeteksi (Clean).</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* 4. Hardware Signal Sent Card */}
          <div className="p-3.5 bg-white rounded-lg border border-slate-200 shadow-xs flex items-center gap-3 text-xs font-mono">
            <Radio
              className={`size-4.5 shrink-0 ${
                rawSignal === "RED"
                  ? "text-rose-600"
                  : rawSignal === "YELLOW"
                  ? "text-amber-500"
                  : "text-emerald-600"
              }`}
            />
            <div className="flex items-center gap-1 flex-wrap">
              <span className="text-gray-600 font-semibold">Hardware Signal Sent:</span>
              <span
                className={`font-bold ${
                  rawSignal === "RED"
                    ? "text-rose-600"
                    : rawSignal === "YELLOW"
                    ? "text-amber-600"
                    : "text-emerald-600"
                }`}
              >
                ● {rawSignal} — Conveyor {rawSignal === "RED" ? "REJECT signal activated" : rawSignal === "YELLOW" ? "SLOW / MANUAL VERIFY signal activated" : "PASS / SORT signal activated"}
              </span>
            </div>
          </div>

          <div className="border-t border-slate-200 my-1" />

          {/* 5. Action Buttons (Re-inspect, Override Decision, Export Record) */}
          <div className="flex flex-col gap-2.5">
            <div className="grid grid-cols-2 gap-3">
              {/* Re-inspect This Lot */}
              <button
                type="button"
                onClick={() => router.push("/inspection")}
                className="py-2.5 px-4 bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold font-sans rounded-sm transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-xs"
              >
                <RotateCcw className="size-3.5" />
                <span>Re-inspect This Lot</span>
              </button>

              {/* Override Decision */}
              <button
                type="button"
                onClick={() => setIsOverrideModalOpen(true)}
                className="py-2.5 px-4 bg-white hover:bg-rose-50 border border-rose-500 text-rose-600 text-xs font-bold font-sans rounded-sm transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-xs"
              >
                <Edit3 className="size-3.5" />
                <span>Override Decision</span>
              </button>
            </div>

            {/* Export This Record Button (Planned for Final) */}
            <div className="flex justify-end">
              <button
                type="button"
                disabled
                title="Available in Final version"
                className="py-2 px-4 bg-white border border-slate-300 text-gray-400 text-xs font-bold font-sans rounded-sm flex items-center justify-center gap-1.5 cursor-not-allowed shadow-none"
              >
                <Download className="size-3.5 text-gray-400" />
                <span>Export This Record</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Override Decision Modal */}
      {isOverrideModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl border border-slate-200 max-w-md w-full p-6 flex flex-col gap-4 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <AlertCircle className="size-5 text-rose-600" />
                <h3 className="text-base font-bold font-sans text-zinc-900">
                  Override Decision (Human-in-the-Loop)
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setIsOverrideModalOpen(false)}
                className="text-gray-400 hover:text-gray-600 p-1 cursor-pointer"
              >
                <X className="size-4" />
              </button>
            </div>

            <p className="text-xs font-sans text-gray-600">
              Sebagai supervisor QC, Anda dapat mengubah status keputusan AI untuk lot{" "}
              <strong className="font-mono">{lot.lotId || lot.lot_id}</strong>.
            </p>

            <div className="flex flex-col gap-3">
              <div>
                <label className="text-xs font-bold font-sans text-gray-700 block mb-1">
                  Keputusan Baru (New Decision)
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {(["PASS", "CONDITIONAL", "FAIL"] as const).map((d) => (
                    <button
                      key={d}
                      type="button"
                      onClick={() => setOverrideDecisionVal(d)}
                      className={`py-2 rounded-sm text-xs font-bold font-sans border transition-all cursor-pointer ${
                        overrideDecisionVal === d
                          ? d === "PASS"
                            ? "bg-emerald-600 text-white border-emerald-600"
                            : d === "CONDITIONAL"
                            ? "bg-amber-500 text-white border-amber-500"
                            : "bg-rose-600 text-white border-rose-600"
                          : "bg-slate-50 text-gray-700 border-slate-300 hover:bg-slate-100"
                      }`}
                    >
                      {d}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-bold font-sans text-gray-700 block mb-1">
                  Alasan Override (Audit Trail Note)
                </label>
                <textarea
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  rows={3}
                  className="w-full bg-slate-50 border border-slate-300 rounded-sm p-2.5 text-xs font-sans text-zinc-900 focus:bg-white focus:outline-sky-600"
                  placeholder="Jelaskan alasan verifikasi visual manual..."
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsOverrideModalOpen(false)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-zinc-700 rounded-sm text-xs font-bold font-sans transition-colors cursor-pointer"
              >
                Batal
              </button>
              <button
                type="button"
                onClick={handleApplyOverride}
                disabled={isOverriding}
                className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-sm text-xs font-bold font-sans transition-colors cursor-pointer flex items-center gap-1.5"
              >
                {isOverriding && <Loader2 className="size-3.5 animate-spin" />}
                <span>Terapkan Override</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
