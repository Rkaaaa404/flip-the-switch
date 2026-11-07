"use client";

import { useEffect, useState } from "react";
import { Hardware } from "@/components/sections/settings-page/Hardware";
import { AIModel } from "@/components/sections/settings-page/AIModel";
import { ExportSettings } from "@/components/sections/settings-page/ExportSettings";
import { BottomSection } from "@/components/sections/settings-page/BottomSection";
import { fetchSettings, saveSettings } from "@/lib/api";
import { CheckCircle2, AlertCircle } from "lucide-react";

const DEFAULT_SETTINGS = {
  mockMode: true,
  cameraSource: "mock",
  ipAddress: "192.168.1.42",
  confidenceThreshold: 65,
  autoExportCSV: false,
  logRetention: "7",
};

export default function SettingsPage() {
  const [mockMode, setMockMode] = useState(DEFAULT_SETTINGS.mockMode);
  const [cameraSource, setCameraSource] = useState(DEFAULT_SETTINGS.cameraSource);
  const [ipAddress, setIpAddress] = useState(DEFAULT_SETTINGS.ipAddress);
  const [confidenceThreshold, setConfidenceThreshold] = useState(DEFAULT_SETTINGS.confidenceThreshold);
  const [autoExportCSV, setAutoExportCSV] = useState(DEFAULT_SETTINGS.autoExportCSV);
  const [logRetention, setLogRetention] = useState(DEFAULT_SETTINGS.logRetention);
  const [saveMessage, setSaveMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    let isMounted = true;
    const loadInitSettings = async () => {
      try {
        const res = await fetchSettings();
        if (isMounted && res) {
          if (res.mock_mode_enabled !== undefined) setMockMode(Boolean(res.mock_mode_enabled));
          if (res.camera_source) setCameraSource(res.camera_source);
          if (res.raspberry_pi_ip) setIpAddress(res.raspberry_pi_ip);
          if (res.confidence_threshold !== undefined || res.confidenceThreshold !== undefined) {
            const rawThresh = Number(res.confidenceThreshold ?? res.confidence_threshold);
            setConfidenceThreshold(rawThresh <= 1.0 ? Math.round(rawThresh * 100) : Math.round(rawThresh));
          }
          if (res.auto_export_csv !== undefined) setAutoExportCSV(Boolean(res.auto_export_csv));
          if (res.log_retention_days) setLogRetention(String(res.log_retention_days));
        }
      } catch (err) {
        console.warn("Failed to fetch initial settings:", err);
      }
    };

    loadInitSettings();
    return () => {
      isMounted = false;
    };
  }, []);

  const handleSave = async () => {
    try {
      await saveSettings({
        mock_mode_enabled: mockMode,
        camera_source: cameraSource,
        raspberry_pi_ip: ipAddress,
        confidence_threshold: confidenceThreshold,
        auto_export_csv: autoExportCSV,
        log_retention_days: Number(logRetention) || 7,
      });
      setSaveMessage({ type: "success", text: "Pengaturan sistem berhasil disimpan ke backend!" });
      setTimeout(() => setSaveMessage(null), 4000);
    } catch (err: any) {
      setSaveMessage({ type: "error", text: "Gagal menyimpan pengaturan ke backend." });
    }
  };

  const handleReset = () => {
    setMockMode(DEFAULT_SETTINGS.mockMode);
    setCameraSource(DEFAULT_SETTINGS.cameraSource);
    setIpAddress(DEFAULT_SETTINGS.ipAddress);
    setConfidenceThreshold(DEFAULT_SETTINGS.confidenceThreshold);
    setAutoExportCSV(DEFAULT_SETTINGS.autoExportCSV);
    setLogRetention(DEFAULT_SETTINGS.logRetention);
    setSaveMessage(null);
  };

  return (
    <div className="flex flex-col gap-6 p-6 max-w-5xl mx-auto w-full">

      {saveMessage && (
        <div
          className={`p-3 rounded-md border flex items-center gap-2 text-sm font-sans ${
            saveMessage.type === "success"
              ? "bg-emerald-50 text-emerald-800 border-emerald-300"
              : "bg-rose-50 text-rose-800 border-rose-300"
          }`}
        >
          {saveMessage.type === "success" ? (
            <CheckCircle2 className="size-4 text-emerald-600 shrink-0" />
          ) : (
            <AlertCircle className="size-4 text-rose-600 shrink-0" />
          )}
          <span>{saveMessage.text}</span>
        </div>
      )}

      <Hardware
        mockMode={mockMode}
        onMockModeChange={setMockMode}
        cameraSource={cameraSource}
        onCameraSourceChange={setCameraSource}
        ipAddress={ipAddress}
        onIpAddressChange={setIpAddress}
      />

      <AIModel
        confidenceThreshold={confidenceThreshold}
        onConfidenceChange={setConfidenceThreshold}
      />

      <ExportSettings
        autoExportCSV={autoExportCSV}
        onAutoExportChange={setAutoExportCSV}
        logRetention={logRetention}
        onLogRetentionChange={setLogRetention}
      />

      <BottomSection onSave={handleSave} onReset={handleReset} />
    </div>
  );
}