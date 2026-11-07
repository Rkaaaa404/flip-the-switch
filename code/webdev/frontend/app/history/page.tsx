"use client";

import { useState } from "react";
import { SearchHistory } from "@/components/sections/lot-history-page/SearchHistory";
import { TableSection } from "@/components/sections/lot-history-page/TableSection";

export default function HistoryPage() {
  const [search, setSearch] = useState("");
  const [family, setFamily] = useState("all");
  const [grade, setGrade] = useState("all");
  const [decision, setDecision] = useState("all");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const handleClearFilters = () => {
    setSearch("");
    setFamily("all");
    setGrade("all");
    setDecision("all");
    setDateFrom("");
    setDateTo("");
  };

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      <SearchHistory
        search={search}
        onSearchChange={setSearch}
        family={family}
        onFamilyChange={setFamily}
        grade={grade}
        onGradeChange={setGrade}
        decision={decision}
        onDecisionChange={setDecision}
        dateFrom={dateFrom}
        onDateFromChange={setDateFrom}
        dateTo={dateTo}
        onDateToChange={setDateTo}
        onClearFilters={handleClearFilters}
      />
      <TableSection
        search={search}
        family={family}
        grade={grade}
        decision={decision}
        dateFrom={dateFrom}
        dateTo={dateTo}
      />
    </div>
  );
}