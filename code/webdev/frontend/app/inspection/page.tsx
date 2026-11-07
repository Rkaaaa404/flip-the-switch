"use client";

import { useState } from "react";
import { FishInspection } from "@/components/sections/inspection-page/FishInspection";
import { ResultSection } from "@/components/sections/inspection-page/ResultSection";
import { InspectionResult } from "@/types";

export default function InspectionPage() {
  const [inspectionResult, setInspectionResult] = useState<InspectionResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleStart = () => {
    setIsLoading(true);
    setErrorMessage(null);
  };

  const handleComplete = (result: InspectionResult) => {
    setIsLoading(false);
    setInspectionResult(result);
    setErrorMessage(null);
  };

  const handleError = (error: string) => {
    setIsLoading(false);
    setErrorMessage(error);
  };

  return (
    <div className="grid gap-6 p-6 grid-cols-1 lg:grid-cols-12 w-full max-w-7xl mx-auto">
      <div className="lg:col-span-7 flex flex-col gap-4">
        <FishInspection
          onInspectionStart={handleStart}
          onInspectionComplete={handleComplete}
          onError={handleError}
          lastResult={inspectionResult}
          isLoading={isLoading}
        />
      </div>
      <div className="lg:col-span-5 flex flex-col gap-4">
        <ResultSection
          result={inspectionResult}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
