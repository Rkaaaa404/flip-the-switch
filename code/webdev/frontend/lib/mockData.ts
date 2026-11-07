export type LotRecord = {
  lotId: string;
  timestamp: string;
  fishFamily: string;
  grade: "A" | "B" | "C";
  defectsCount: number;
  decision: "PASS" | "FAIL";
  confidence: number;
};

// TODO: Replace with actual data from GET /api/v1/lots
export const MOCK_LOTS: LotRecord[] = [
  { lotId: "LOT-2026-0730-006", timestamp: "10:42:31", fishFamily: "Scombridae", grade: "A", defectsCount: 0, decision: "PASS", confidence: 91.2 },
  { lotId: "LOT-2026-0730-005", timestamp: "10:38:14", fishFamily: "Cichlidae",  grade: "B", defectsCount: 1, decision: "PASS", confidence: 87.4 },
  { lotId: "LOT-2026-0730-004", timestamp: "10:31:05", fishFamily: "Scombridae", grade: "A", defectsCount: 0, decision: "PASS", confidence: 94.8 },
  { lotId: "LOT-2026-0730-003", timestamp: "10:24:50", fishFamily: "Scombridae", grade: "C", defectsCount: 2, decision: "FAIL", confidence: 61.2 },
  { lotId: "LOT-2026-0730-002", timestamp: "10:18:33", fishFamily: "Cichlidae",  grade: "B", defectsCount: 1, decision: "PASS", confidence: 79.3 },
  { lotId: "LOT-2026-0730-001", timestamp: "10:11:22", fishFamily: "Scombridae", grade: "A", defectsCount: 0, decision: "PASS", confidence: 95.1 },
  { lotId: "LOT-2026-0729-108", timestamp: "09:58:41", fishFamily: "Cichlidae",  grade: "C", defectsCount: 3, decision: "FAIL", confidence: 58.7 },
  { lotId: "LOT-2026-0729-107", timestamp: "09:44:12", fishFamily: "Scombridae", grade: "B", defectsCount: 1, decision: "PASS", confidence: 82.6 },
];
