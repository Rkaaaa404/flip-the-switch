export type Decision = "PASS" | "FAIL" | "CONDITIONAL";
export type HardwareSignal = "GREEN" | "YELLOW" | "RED";
export type Grade = "A" | "B" | "C";

export type DefectLabel = 
  | "sisik_sisa" 
  | "warna_abnormal" 
  | "luka_robekan" 
  | "lendir_berlebih"
  | string;

export interface Defect {
  label: DefectLabel;
  bbox: [number, number, number, number]; // [x1, y1, x2, y2] in original image space
  confidence: number;
}

export interface InspectionResult {
  lotId: string;
  lot_id?: string;
  timestamp: string;
  family: string;
  fishFamily?: string;
  fish_family?: string;
  grade: Grade;
  confidence: number;
  grade_confidence?: number;
  defects: Defect[];
  decision: Decision;
  conveyorSignal: HardwareSignal;
  hardware_signal?: HardwareSignal;
  processingTimeMs: number;
  processing_time_ms?: number;
  imageUrl?: string;
  image_url?: string;
  freshnessNote?: string;
  storage_slot?: string;
  storageSlot?: string;
}

export interface LotRecord {
  id: number;
  lotId: string;
  lot_id?: string;
  timestamp: string;
  family: string;
  fishFamily?: string;
  fish_family?: string;
  grade: Grade;
  confidence: number;
  grade_confidence?: number;
  defectsCount: number;
  defects_count?: number;
  decision: Decision;
  conveyorSignal: HardwareSignal;
  hardware_signal?: HardwareSignal;
  imageUrl?: string;
  image_path?: string;
  processing_time_ms?: number;
  processingTimeMs?: number;
  defects?: Defect[];
  storage_slot?: string;
  storageSlot?: string;
  storage_zone?: string;
  storageZone?: string;
  stored_at?: string;
  storedAt?: string;
  dispatch_id?: string;
  dispatchId?: string;
  dispatched_at?: string;
  dispatchedAt?: string;
  inspector_note?: string;
  inspectorNote?: string;
  reason_summary?: string;
  reasonSummary?: string;
}

export interface DashboardStats {
  total_inspected_today: number;
  totalInspectedToday?: number;
  current_lot_id: string;
  currentLotId?: string;
  pass_rate: number;
  passRate?: number;
  pass_rate_delta: number;
  passRateDelta?: number;
  fail_rate: number;
  failRate?: number;
  fail_rate_delta: number;
  failRateDelta?: number;
  avg_confidence: number;
  avg_confidence_score?: number;
  avgConfidence?: number;
}

export interface HardwareStatus {
  camera: string;
  conveyor_relay?: string;
  conveyor?: string;
  tower_light?: string;
  towerLight?: string;
  buzzer?: string;
  mock_mode: boolean;
  mockMode?: boolean;
  mockModeEnabled?: boolean;
}

// Storage Map Types
export type StorageZone = "cold" | "frozen";

export interface StorageSlot {
  slot_id: string;
  slotId?: string;
  zone: StorageZone;
  lot_id?: string | null;
  lotId?: string | null;
  assigned_at?: string | null;
  assignedAt?: string | null;
  assigned_by?: string;
  assignedBy?: string;
  lot?: LotRecord | null;
}

export interface StorageOverview {
  total_slots: number;
  totalSlots?: number;
  occupied: number;
  available: number;
  pending_assignment: number;
  pendingAssignment?: number;
  slots: StorageSlot[];
}

// Dispatch Types (3-stage lifecycle: Pending -> In Transit -> Delivered)
export type DispatchStatus = "pending" | "in_transit" | "delivered" | "dispatched" | string;

export interface DispatchRecord {
  dispatch_id: string;
  dispatchId?: string;
  buyer_name: string;
  buyerName?: string;
  destination: string;
  container_no?: string | null;
  containerNo?: string | null;
  dispatch_date: string;
  dispatchDate?: string;
  status: DispatchStatus;
  notes?: string | null;
  lots_count?: number;
  lotsCount?: number;
  created_at?: string;
  createdAt?: string;
  lots?: LotRecord[];
  qc_summary?: {
    total_lots: number;
    all_passed: boolean;
    avg_confidence: number;
    total_defects: number;
  };
}