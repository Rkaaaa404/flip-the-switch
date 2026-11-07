import {
  InspectionResult,
  LotRecord,
  DashboardStats,
  HardwareStatus,
  StorageOverview,
  StorageSlot,
  DispatchRecord,
} from "@/types";

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Helper to convert backend relative image paths (/uploads/...) to full browser URLs
export function getFullImageUrl(path?: string): string {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `${API_BASE}${path}`;
}

export async function runInspection(imageFile: File, fishFamily: string, lotId?: string): Promise<InspectionResult> {
  const formData = new FormData();
  formData.append("image", imageFile);
  formData.append("fish_family", fishFamily);
  formData.append("family", fishFamily);
  if (lotId) formData.append("lot_id", lotId);

  const res = await fetch(`${API_BASE}/api/v1/inspections/run`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Inspection request failed");
  }
  return res.json();
}

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE}/api/v1/dashboard/stats`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch dashboard statistics");
  return res.json();
}

export async function fetchRecentLots(limit = 5): Promise<LotRecord[]> {
  const res = await fetch(`${API_BASE}/api/v1/lots/recent?limit=${limit}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch recent lot inspections");
  return res.json();
}

export async function fetchLots(params: {
  search?: string;
  family?: string;
  grade?: string;
  decision?: string;
  from?: string;
  to?: string;
  date_from?: string;
  date_to?: string;
  page?: number;
  limit?: number;
}) {
  const query = new URLSearchParams();
  if (params.search) query.set("search", params.search);
  if (params.family) query.set("family", params.family);
  if (params.grade) query.set("grade", params.grade);
  if (params.decision) query.set("decision", params.decision);
  const fromVal = params.from || params.date_from;
  const toVal = params.to || params.date_to;
  if (fromVal) query.set("from", fromVal);
  if (toVal) query.set("to", toVal);
  if (params.page) query.set("page", params.page.toString());
  if (params.limit) query.set("limit", params.limit.toString());

  const res = await fetch(`${API_BASE}/api/v1/lots?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch lot history");
  return res.json();
}

export async function fetchLotDetail(lotId: string): Promise<LotRecord> {
  const res = await fetch(`${API_BASE}/api/v1/lots/${lotId}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Lot record '${lotId}' not found`);
  return res.json();
}

export const fetchLotById = fetchLotDetail;

export async function updateLotNote(lotId: string, note: string): Promise<{ status: string; message: string; inspector_note: string }> {
  const res = await fetch(`${API_BASE}/api/v1/lots/${lotId}/note`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to update note" }));
    throw new Error(err.detail || "Failed to update note");
  }
  return res.json();
}

export async function overrideLotDecision(lotId: string, decision: "PASS" | "FAIL" | "CONDITIONAL", reason: string): Promise<{ status: string; message: string; decision: string; hardware_signal: string }> {
  const res = await fetch(`${API_BASE}/api/v1/lots/${lotId}/override`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, reason }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to override decision" }));
    throw new Error(err.detail || "Failed to override decision");
  }
  return res.json();
}

export async function deleteLot(lotId: string): Promise<{ status: string; message: string }> {
  const res = await fetch(`${API_BASE}/api/v1/lots/${lotId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `Failed to delete lot '${lotId}'` }));
    throw new Error(err.detail || `Failed to delete lot '${lotId}'`);
  }
  return res.json();
}

export async function fetchHardwareStatus(): Promise<HardwareStatus> {
  const res = await fetch(`${API_BASE}/api/v1/hardware/status`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch hardware status");
  return res.json();
}

export async function fetchModelsStatus() {
  const res = await fetch(`${API_BASE}/api/v1/settings/models/status`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch AI models status");
  return res.json();
}

export async function fetchSettings() {
  const res = await fetch(`${API_BASE}/api/v1/settings`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load settings");
  return res.json();
}

export async function saveSettings(payload: any) {
  const res = await fetch(`${API_BASE}/api/v1/settings`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to save settings");
  return res.json();
}

export async function testDeviceConnection(ipAddress: string) {
  const res = await fetch(`${API_BASE}/api/v1/hardware/test-connection`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ipAddress }),
  });
  return res.json();
}

export function getExportCsvUrl(params?: { from?: string; to?: string; family?: string }): string {
  const query = new URLSearchParams();
  if (params?.from) query.set("from", params.from);
  if (params?.to) query.set("to", params.to);
  if (params?.family) query.set("family", params.family);
  return `${API_BASE}/api/v1/lots/export/csv?${query.toString()}`;
}

// ----------------------------------------------------
// STORAGE API METHODS
// ----------------------------------------------------

export async function fetchStorageSlots(): Promise<StorageOverview> {
  const res = await fetch(`${API_BASE}/api/v1/storage/slots`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch storage slots");
  return res.json();
}

export async function fetchPendingStorageLots(): Promise<LotRecord[]> {
  const res = await fetch(`${API_BASE}/api/v1/storage/pending`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch pending storage lots");
  return res.json();
}

export async function assignStorageSlot(slotId: string, lotId: string) {
  const res = await fetch(`${API_BASE}/api/v1/storage/assign`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slot_id: slotId, lot_id: lotId }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to assign slot" }));
    throw new Error(err.detail || "Failed to assign storage slot");
  }
  return res.json();
}

export async function clearStorageSlot(slotId: string) {
  const res = await fetch(`${API_BASE}/api/v1/storage/slots/${slotId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`Failed to clear slot ${slotId}`);
  return res.json();
}

// ----------------------------------------------------
// DISPATCH API METHODS
// ----------------------------------------------------

export async function fetchDispatches(): Promise<{
  total_dispatches: number;
  totalDispatches?: number;
  pending: number;
  in_transit?: number;
  inTransit?: number;
  dispatched: number;
  delivered: number;
  items: DispatchRecord[];
}> {
  const res = await fetch(`${API_BASE}/api/v1/dispatch`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch dispatches");
  return res.json();
}

export async function fetchAvailableLotsForDispatch(): Promise<LotRecord[]> {
  const res = await fetch(`${API_BASE}/api/v1/dispatch/available-lots`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch available lots for dispatch");
  return res.json();
}

export async function fetchDispatchDetail(dispatchId: string): Promise<DispatchRecord> {
  const res = await fetch(`${API_BASE}/api/v1/dispatch/${dispatchId}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch dispatch ${dispatchId}`);
  return res.json();
}

export async function createDispatch(payload: {
  buyer_name: string;
  destination: string;
  container_no?: string;
  dispatch_date?: string;
  lot_ids: string[];
  notes?: string;
}) {
  const res = await fetch(`${API_BASE}/api/v1/dispatch`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to create dispatch" }));
    throw new Error(err.detail || "Failed to create dispatch");
  }
  return res.json();
}

export async function updateDispatchStatus(dispatchId: string, status: "pending" | "in_transit" | "delivered" | string) {
  const res = await fetch(`${API_BASE}/api/v1/dispatch/${dispatchId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) throw new Error(`Failed to update dispatch status to ${status}`);
  return res.json();
}