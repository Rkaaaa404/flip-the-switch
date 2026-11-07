"use client";

import React, { useRef, useState, useEffect, useCallback } from "react";
import {
  Camera,
  Upload,
  Plus,
  Loader2,
  RefreshCw,
  RotateCcw,
  AlertCircle,
  CheckCircle2,
  Video,
  X,
  FlipHorizontal,
  CircleDot,
  Radio,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { runInspection } from "@/lib/api";
import { InspectionResult } from "@/types";

export const FISH_TYPES = [
  { id: "Tuna", label: "Tuna (Thunnini / Tuna)" },
  { id: "Mackarel", label: "Mackarel (Scomber / Mackarel / Kembung)" },
  { id: "Nila", label: "Nila (Oreochromis niloticus / Tilapia)" },
];

export const FISH_FAMILIES = FISH_TYPES;

// Color mapping for defect bounding boxes
const DEFECT_COLOR_MAP: Record<string, { border: string; bg: string; text: string }> = {
  parasite: {
    border: "border-amber-400",
    bg: "bg-amber-400",
    text: "text-zinc-900",
  },
  discoloration: {
    border: "border-purple-400",
    bg: "bg-purple-400",
    text: "text-white",
  },
  lesion: {
    border: "border-rose-500",
    bg: "bg-rose-500",
    text: "text-white",
  },
  slime: {
    border: "border-sky-400",
    bg: "bg-sky-400",
    text: "text-zinc-900",
  },
};

type FishInspectionProps = {
  onInspectionStart?: () => void;
  onInspectionComplete?: (result: InspectionResult) => void;
  onError?: (error: string) => void;
  lastResult?: InspectionResult | null;
  isLoading?: boolean;
};

export const FishInspection = ({
  onInspectionStart,
  onInspectionComplete,
  onError,
  lastResult,
  isLoading = false,
}: FishInspectionProps) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedFishType, setSelectedFishType] = useState<string>("Tuna");
  const [imageDimensions, setImageDimensions] = useState<{ naturalWidth: number; naturalHeight: number } | null>(null);
  const [localError, setLocalError] = useState<string | null>(null);

  // Camera stream state
  const [isCameraActive, setIsCameraActive] = useState<boolean>(false);
  const [isCameraLoading, setIsCameraLoading] = useState<boolean>(false);
  const [facingMode, setFacingMode] = useState<"environment" | "user">("environment");

  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  // Stop camera helper
  const stopCameraStream = useCallback(() => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
    setIsCameraLoading(false);
  }, []);

  // Cleanup camera stream on unmount
  useEffect(() => {
    return () => {
      stopCameraStream();
    };
  }, [stopCameraStream]);

  // Start camera stream
  const startCamera = async (mode: "environment" | "user" = facingMode) => {
    setLocalError(null);
    setIsCameraLoading(true);
    stopCameraStream();

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Browser Anda tidak mendukung akses kamera langsung (WebRTC).");
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: mode,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });

      mediaStreamRef.current = stream;
      setIsCameraActive(true);
      setFacingMode(mode);
    } catch (err: any) {
      console.warn("Camera access error:", err);
      let message = "Gagal mengakses kamera. Pastikan izin kamera telah diberikan.";
      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
        message = "Akses kamera ditolak oleh browser. Mohon izinkan akses kamera di pengaturan browser.";
      } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
        message = "Kamera tidak terdeteksi pada perangkat ini.";
      }
      setLocalError(message);
      setIsCameraActive(false);
    } finally {
      setIsCameraLoading(false);
    }
  };

  // Ensure video stream connects reliably as soon as video element is mounted
  useEffect(() => {
    if (isCameraActive && videoRef.current && mediaStreamRef.current) {
      const video = videoRef.current;
      video.srcObject = mediaStreamRef.current;
      video.onloadedmetadata = () => {
        video.play().catch((err) => console.warn("Video play error:", err));
      };
    }
  }, [isCameraActive]);

  const handleToggleFacingMode = () => {
    const nextMode = facingMode === "environment" ? "user" : "environment";
    startCamera(nextMode);
  };

  const handleCaptureSnapshot = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const width = video.videoWidth || 1280;
    const height = video.videoHeight || 720;

    canvas.width = width;
    canvas.height = height;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, width, height);

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setLocalError("Gagal mengambil snapshot dari video feed.");
          return;
        }

        const filename = `camera_snapshot_${Date.now()}.jpg`;
        const file = new File([blob], filename, { type: "image/jpeg" });
        const objectUrl = URL.createObjectURL(blob);

        setSelectedFile(file);
        setPreviewUrl(objectUrl);
        stopCameraStream();
        setLocalError(null);
      },
      "image/jpeg",
      0.92
    );
  };

  const handleUploadClick = () => {
    setLocalError(null);
    stopCameraStream();
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setLocalError("Format berkas tidak valid. Harap pilih gambar JPG, PNG, atau WEBP.");
      return;
    }

    setLocalError(null);
    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    stopCameraStream();
  };

  const handleImageLoaded = (e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    setImageDimensions({
      naturalWidth: img.naturalWidth || 640,
      naturalHeight: img.naturalHeight || 480,
    });
  };

  const handleReInspect = () => {
    stopCameraStream();
    setPreviewUrl(null);
    setSelectedFile(null);
    setImageDimensions(null);
    setLocalError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleRunInspection = async () => {
    if (!selectedFile && !previewUrl) {
      setLocalError("Pilih, foto, atau unggah sampel ikan terlebih dahulu.");
      return;
    }

    setLocalError(null);
    onInspectionStart?.();

    try {
      let fileToSend = selectedFile;
      if (!fileToSend && previewUrl) {
        const response = await fetch(previewUrl);
        const blob = await response.blob();
        fileToSend = new File([blob], `fish_${selectedFishType.toLowerCase()}.jpg`, { type: "image/jpeg" });
      }

      if (!fileToSend) {
        throw new Error("Berkas gambar tidak ditemukan.");
      }

      const result = await runInspection(fileToSend, selectedFishType);
      onInspectionComplete?.(result);
    } catch (err: any) {
      const msg = err?.message || "Gagal melakukan inspeksi AI. Pastikan backend aktif.";
      setLocalError(msg);
      onError?.(msg);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] outline outline-1 outline-slate-300 p-6 flex flex-col gap-4">
      {/* Hidden Canvas for Snapshot extraction */}
      <canvas ref={canvasRef} className="hidden" />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Camera className="size-5 text-sky-700" />
          <h2 className="text-lg font-bold font-sans text-zinc-900">
            Fish Inspection Viewfinder
          </h2>
        </div>

        {/* Action button in Header */}
        {previewUrl ? (
          <Button
            variant="outline-sky"
            size="sm"
            onClick={handleReInspect}
            disabled={isLoading}
            className="flex items-center gap-1.5 cursor-pointer text-xs"
          >
            <RotateCcw className="size-3.5" />
            <span>Ganti Sampel</span>
          </Button>
        ) : isCameraActive ? (
          <Button
            variant="outline-sky"
            size="sm"
            onClick={stopCameraStream}
            className="flex items-center gap-1.5 cursor-pointer text-xs text-red-600 border-red-200 hover:bg-red-50"
          >
            <X className="size-3.5" />
            <span>Tutup Kamera</span>
          </Button>
        ) : null}
      </div>

      {/* Error Alert Banner */}
      {localError && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md flex items-center gap-2 text-sm text-red-700">
          <AlertCircle className="size-4 shrink-0 text-red-600" />
          <span>{localError}</span>
        </div>
      )}

      {/* Main View Area: Image Preview OR Camera Live Feed OR Initial Action State */}
      <div className="relative w-full h-[360px] bg-slate-900 rounded-md outline outline-1 outline-slate-300 overflow-hidden flex items-center justify-center">
        {/* CASE 1: Camera Stream is Active */}
        {isCameraActive ? (
          <div className="relative w-full h-full flex items-center justify-center bg-black">
            <video
              ref={(el) => {
                videoRef.current = el;
                if (el && mediaStreamRef.current && el.srcObject !== mediaStreamRef.current) {
                  el.srcObject = mediaStreamRef.current;
                  el.play().catch(() => {});
                }
              }}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />

            {/* Top Controls: Flip & Close */}
            <div className="absolute top-3 right-3 flex items-center gap-2 pointer-events-auto z-10">
              <button
                type="button"
                onClick={handleToggleFacingMode}
                className="p-2 bg-black/60 hover:bg-black/80 text-white rounded-full transition-colors cursor-pointer"
                title="Ganti Kamera"
              >
                <FlipHorizontal className="size-4" />
              </button>
              <button
                type="button"
                onClick={stopCameraStream}
                className="p-2 bg-black/60 hover:bg-black/80 text-white rounded-full transition-colors cursor-pointer"
                title="Tutup Kamera"
              >
                <X className="size-4" />
              </button>
            </div>

            {/* Bottom Capture Button Bar */}
            <div className="absolute bottom-4 left-0 right-0 flex items-center justify-center gap-4 pointer-events-auto z-10">
              <button
                type="button"
                onClick={handleCaptureSnapshot}
                className="flex items-center gap-2 px-6 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm font-sans rounded-full shadow-lg transition-all active:scale-95 cursor-pointer border-2 border-white"
              >
                <Camera className="size-4.5 text-white" />
                <span>Ambil Foto</span>
              </button>
            </div>
          </div>
        ) : previewUrl ? (
          /* CASE 2: Image Preview with Bounding Box Overlay */
          <div className="relative w-full h-full flex items-center justify-center">
            <img
              src={previewUrl}
              alt="Fish sample preview"
              onLoad={handleImageLoaded}
              className="w-full h-full object-contain"
            />

            {/* Dynamic YOLOv8 Bounding Box Overlays */}
            {lastResult && lastResult.defects && lastResult.defects.length > 0 && imageDimensions && (
              <div className="absolute inset-0 pointer-events-none">
                {lastResult.defects.map((defect, idx) => {
                  const [x1, y1, x2, y2] = defect.bbox;
                  const nw = imageDimensions.naturalWidth || 640;
                  const nh = imageDimensions.naturalHeight || 480;

                  const leftPct = (x1 / nw) * 100;
                  const topPct = (y1 / nh) * 100;
                  const widthPct = Math.max(2, ((x2 - x1) / nw) * 100);
                  const heightPct = Math.max(2, ((y2 - y1) / nh) * 100);

                  const styleInfo = DEFECT_COLOR_MAP[defect.label] || {
                    border: "border-red-600",
                    bg: "bg-red-600",
                    text: "text-white",
                  };

                  return (
                    <div
                      key={`${defect.label}-${idx}`}
                      className={`absolute border-2 ${styleInfo.border} rounded-xs transition-all`}
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
                        {defect.label} {(defect.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        ) : (
          /* CASE 3: Initial Empty State (Choose Camera or File Upload) */
          <div className="w-full h-full bg-slate-50 flex flex-col items-center justify-center p-6 text-center">
            <div className="max-w-md flex flex-col items-center gap-4">
              <div>
                <p className="text-base font-bold font-sans text-zinc-900">
                  Ambil Snapshot Kamera atau Unggah Sampel
                </p>
                <p className="text-xs font-normal font-sans text-gray-500 mt-1">
                  Pilih metode pengambilan citra ikan untuk proses klasifikasi kesegaran dan deteksi cacat mutu.
                </p>
              </div>

              {/* Action Buttons: Camera vs File Upload */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full pt-1">
                {/* 1. Live Camera Button */}
                <button
                  type="button"
                  onClick={() => startCamera("environment")}
                  disabled={isCameraLoading}
                  className="flex flex-col items-center justify-center gap-2 p-4 rounded-lg bg-sky-50 border-2 border-sky-300 hover:border-sky-500 hover:bg-sky-100 transition-all cursor-pointer group shadow-xs"
                >
                  <div className="size-11 rounded-full bg-sky-600 text-white flex items-center justify-center group-hover:scale-105 transition-transform shadow-xs">
                    {isCameraLoading ? (
                      <Loader2 className="size-5 animate-spin" />
                    ) : (
                      <Video className="size-5" />
                    )}
                  </div>
                  <div>
                    <span className="text-xs font-bold font-sans text-sky-900 block">
                      Akses Kamera Feed
                    </span>
                    <span className="text-[10px] font-sans text-sky-700 block mt-0.5">
                      Buka Web Camera & Ambil Foto
                    </span>
                  </div>
                </button>

                {/* 2. File Upload Button */}
                <button
                  type="button"
                  onClick={handleUploadClick}
                  className="flex flex-col items-center justify-center gap-2 p-4 rounded-lg bg-white border-2 border-slate-300 hover:border-slate-400 hover:bg-slate-50 transition-all cursor-pointer group shadow-xs"
                >
                  <div className="size-11 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <Upload className="size-5" />
                  </div>
                  <div>
                    <span className="text-xs font-bold font-sans text-zinc-900 block">
                      Unggah Berkas Gambar
                    </span>
                    <span className="text-[10px] font-sans text-gray-500 block mt-0.5">
                      Pilih file JPEG/PNG/WEBP
                    </span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Loading Overlay */}
        {isLoading && (
          <div className="absolute inset-0 bg-slate-900/70 backdrop-blur-xs flex flex-col items-center justify-center gap-3 text-white z-20">
            <Loader2 className="size-9 animate-spin text-sky-400" />
            <div className="text-center">
              <p className="text-sm font-semibold font-sans">Mengeksekusi Inferensi AI...</p>
              <p className="text-xs font-mono text-slate-300">MobileNetV3 (Freshness) + YOLOv8s (Defects)</p>
            </div>
          </div>
        )}
      </div>

      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Controls Row: Fish Type Selector */}
      <div className="flex items-end gap-4 pt-2 border-t border-slate-100">
        <div className="flex-1 flex flex-col gap-1">
          <label className="text-xs font-bold font-sans text-gray-700 tracking-wide">
            Jenis Ikan (Fish Type Category)
          </label>
          <select
            value={selectedFishType}
            onChange={(e) => setSelectedFishType(e.target.value)}
            className="w-full px-3 py-2 bg-slate-50 rounded-sm outline outline-1 outline-slate-300 text-sm font-sans font-medium text-zinc-900 cursor-pointer focus:outline-sky-500"
          >
            {FISH_TYPES.map((f) => (
              <option key={f.id} value={f.id} className="font-sans text-zinc-900">
                {f.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Run Inspection Button */}
      <Button
        variant="primary"
        size="lg"
        disabled={isLoading || (!previewUrl && !selectedFile)}
        className="w-full uppercase tracking-wide font-bold flex items-center justify-center gap-2 py-3 cursor-pointer mt-1"
        onClick={handleRunInspection}
      >
        {isLoading ? (
          <>
            <Loader2 className="size-5 animate-spin" />
            <span>Memproses Inferensi AI...</span>
          </>
        ) : (
          <>
            <CheckCircle2 className="size-5" />
            <span>Jalankan Inspeksi AI (Run Inspection)</span>
          </>
        )}
      </Button>

      {/* AI Governance Disclaimer */}
      <p className="text-[11px] text-gray-400 font-sans text-center italic">
        AI adalah sistem pendukung keputusan QC, bukan pengganti mutlak penilaian akhir operator manusia.
      </p>
    </div>
  );
};

