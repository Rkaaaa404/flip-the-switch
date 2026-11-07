import type { Defect } from "@/types";

export type QuantityUnit = "kg" | "count";

export type DeliveryStatus =
  | "active_receiving"
  | "inspection_complete"
  | "disposition_recorded"
  | "closed";

export type InspectionStatus =
  | "COMPLETE"
  | "PARTIAL_DORSAL_ONLY"
  | "PARTIAL_VENTRAL_ONLY"
  | "FAILED_CAPTURE";

export type ViewSide = "dorsal" | "ventral";

export type FreshnessGrade = "A" | "B" | "C" | "UNSUPPORTED";

export type InferenceMode = "real_onnx" | "simulated_mock" | "skipped_unsupported";

export type DispositionOutcome = "ACCEPT" | "REJECT" | "REPROCESS" | "DOWNGRADE";

export type ProcessingStage =
  | "receiving_to_storage"
  | "receiving_to_processing"
  | "processing_wggs"
  | "processing_fillet"
  | "storage_to_processing"
  | "processing_to_dispatch";

export type MissingLinkKind =
  | "PARTIAL_INSPECTION"
  | "FLAGGED_WITHOUT_DISPOSITION"
  | "UNDISPOSITIONED_QUANTITY"
  | "DISPOSITION_LOT_NOT_HANDED_OFF"
  | "LOT_LOCATION_UNKNOWN"
  | "NO_UPSTREAM_MOVEMENT"
  | "DELIVERY_NOT_FOUND";

export interface DeliveryCreate {
  supplier_name: string;
  species: string;
  fish_family: string;
  stated_quantity: number;
  quantity_unit: QuantityUnit;
  truck_identifier?: string | null;
  created_by: string;
  received_at?: string | null;
}

export interface Delivery {
  id: string;
  supplier_name: string;
  species: string;
  fish_family: string;
  received_at: string;
  stated_quantity: number;
  quantity_unit: QuantityUnit;
  truck_identifier: string | null;
  status: DeliveryStatus;
  created_by: string;
  created_at: string;
}

export interface DeliverySummary extends Delivery {
  total_inspected: number;
  flagged_count: number;
  partial_count: number;
}

export interface DeliveryListResponse {
  items: DeliverySummary[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface InspectionView {
  id: string;
  view_side: ViewSide;
  image_path: string;
  sha256: string;
  freshness_grade: FreshnessGrade;
  freshness_confidence: number;
  defects: Defect[];
  inference_mode: InferenceMode;
  inference_latency_ms: number;
  created_at: string;
}

export interface FishInspection {
  id: string;
  sequence_in_delivery: number;
  status: InspectionStatus;
  flagged_for_review: boolean;
  flag_reasons: string[];
  created_at: string;
  views: InspectionView[];
}

export interface HumanDispositionCreate {
  output_lot_id?: string | null;
  disposition: DispositionOutcome;
  affected_quantity: number;
  quantity_unit: QuantityUnit;
  decision_reason: string;
  authorized_by: string;
  supersedes_id?: number | null;
}

export interface HumanDisposition {
  id: number;
  delivery_id: string;
  output_lot_id: string | null;
  disposition: DispositionOutcome;
  affected_quantity: number;
  quantity_unit: QuantityUnit;
  decision_reason: string;
  authorized_by: string;
  decided_at: string;
  supersedes_id: number | null;
  superseded: boolean;
  /** "switch_gate" when signed by a person in the Switch room via qc-gate. */
  authorized_via?: string | null;
  switch_message_id?: string | null;
}

export interface MaterialMovementCreate {
  input_ref: string;
  output_lot_id: string;
  stage: ProcessingStage;
  quantity_in: number;
  quantity_out: number;
  quantity_unit: QuantityUnit;
  normal_yield_loss?: number;
  qc_reject_loss?: number;
  unexplained_variance?: number;
  operator_id: string;
  notes?: string | null;
}

export interface MaterialMovement {
  id: number;
  delivery_id: string;
  input_ref: string;
  output_lot_id: string;
  stage: ProcessingStage;
  quantity_in: number;
  quantity_out: number;
  quantity_unit: QuantityUnit;
  normal_yield_loss: number;
  qc_reject_loss: number;
  unexplained_variance: number;
  operator_id: string;
  timestamp: string;
  notes: string | null;
  authorized_via?: string | null;
  switch_message_id?: string | null;
}

export interface StorageSlotRef {
  slot_id: string;
  zone: string;
  assigned_at: string | null;
}

export interface DispatchRef {
  dispatch_id: string;
  buyer_name: string;
  destination: string;
  status: string;
  dispatch_date: string;
}

export interface MovementNode extends MaterialMovement {
  storage_slots: StorageSlotRef[];
  dispatches: DispatchRef[];
}

export interface MissingLink {
  kind: MissingLinkKind;
  ref: string;
  detail: string;
}

export interface InspectionSummary {
  total: number;
  complete: number;
  partial_dorsal_only: number;
  partial_ventral_only: number;
  failed_capture: number;
  flagged: number;
}

export interface QuantityBalance {
  stated_quantity: number;
  quantity_unit: QuantityUnit;
  dispositioned_quantity: number;
  allocated_from_intake: number;
  unallocated_quantity: number;
}

export interface DeliveryDetail {
  delivery: DeliverySummary;
  inspections: FishInspection[];
  inspections_total: number;
  page: number;
  limit: number;
  dispositions: HumanDisposition[];
  movements: MaterialMovement[];
}

export interface DeliveryTraceTree {
  delivery: Delivery;
  inspection_summary: InspectionSummary;
  dispositions: HumanDisposition[];
  movements: MovementNode[];
  balance: QuantityBalance;
  missing_links: MissingLink[];
}

export interface LotProvenance {
  lot_id: string;
  delivery: Delivery | null;
  chain: MaterialMovement[];
  missing_links: MissingLink[];
}

export interface SimulateRequest {
  count?: number;
  drop_ventral_every?: number | null;
}

export type ProposalStatus = "pending" | "applied" | "rejected";

/** A draft written by qc-agent in the Switch room. Only a person's `@qc-gate` command applies it. */
export interface RecordProposal {
  id: string; // DP-n or MV-n
  kind: "disposition" | "movement";
  delivery_id: string;
  payload: Record<string, unknown>;
  status: ProposalStatus;
  source_message_id: string | null;
  created_at: string;
  decided_by: string | null;
  decided_at: string | null;
  decision_note: string | null;
  applied_record_id: number | null;
  approve_command: string;
}
