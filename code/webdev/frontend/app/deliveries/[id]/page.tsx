"use client";

import { useCallback, useEffect, useState, type FormEvent, type ReactNode } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { AlertCircle, Loader2 } from "lucide-react";
import {
  captureView,
  getDeliveryById,
  getFullImageUrl,
  getProposals,
  simulateConveyor,
  updateDeliveryStatus,
} from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type { Defect } from "@/types";
import type {
  DeliveryDetail,
  DeliveryStatus,
  DeliverySummary,
  DispositionOutcome,
  FishInspection,
  HumanDisposition,
  InferenceMode,
  InspectionStatus,
  InspectionView,
  MaterialMovement,
  ProcessingStage,
  RecordProposal,
  ViewSide,
} from "@/types/delivery";

const POLL_MS = 3000;

type Tone = "green" | "amber" | "red" | "grey" | "sky" | "orange";
type Feedback = { tone: "error" | "success"; text: string } | null;

const STATUS_LABEL: Record<DeliveryStatus, string> = {
  active_receiving: "Active receiving",
  inspection_complete: "Inspection complete",
  disposition_recorded: "Disposition recorded",
  closed: "Closed",
};

const DELIVERY_STATUS_TONE: Record<DeliveryStatus, Tone> = {
  active_receiving: "sky",
  inspection_complete: "amber",
  disposition_recorded: "orange",
  closed: "grey",
};

const INSPECTION_STATUS_TONE: Record<InspectionStatus, Tone> = {
  COMPLETE: "green",
  PARTIAL_DORSAL_ONLY: "amber",
  PARTIAL_VENTRAL_ONLY: "amber",
  FAILED_CAPTURE: "red",
};

const MISSING_VIEW_WARNING: Partial<Record<InspectionStatus, string>> = {
  PARTIAL_DORSAL_ONLY: "Missing ventral view",
  PARTIAL_VENTRAL_ONLY: "Missing dorsal view",
  FAILED_CAPTURE: "Capture failed: no usable views",
};

const INFERENCE_LABEL: Record<InferenceMode, string> = {
  real_onnx: "Real ONNX",
  simulated_mock: "Simulated mock",
  skipped_unsupported: "Skipped (unsupported)",
};

const OUTCOME_TONE: Record<DispositionOutcome, Tone> = {
  ACCEPT: "green",
  REJECT: "red",
  REPROCESS: "amber",
  DOWNGRADE: "orange",
};

const STAGE_LABEL: Record<ProcessingStage, string> = {
  receiving_to_storage: "Receiving → storage",
  receiving_to_processing: "Receiving → processing",
  processing_wggs: "Processing (WGGS)",
  processing_fillet: "Processing (fillet)",
  storage_to_processing: "Storage → processing",
  processing_to_dispatch: "Processing → dispatch",
};

const TONE_CLASS: Record<Tone, string> = {
  green: "bg-emerald-100 text-emerald-700 border-emerald-200",
  amber: "bg-amber-100 text-amber-700 border-amber-200",
  red: "bg-red-100 text-red-700 border-red-200",
  grey: "bg-gray-100 text-gray-600 border-gray-200",
  sky: "bg-sky-100 text-sky-700 border-sky-200",
  orange: "bg-orange-100 text-orange-700 border-orange-200",
};

const INPUT_CLASS =
  "h-10 rounded-md border border-gray-300 bg-white px-3 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-orange-500";
const LABEL_CLASS = "flex flex-col gap-1 text-xs font-medium text-gray-600";

function errorMessage(err: unknown): string {
  return err instanceof Error && err.message ? err.message : "Request failed.";
}

function formatTime(iso: string): string {
  const date = new Date(iso);
  return Number.isNaN(date.getTime()) ? iso : date.toLocaleString();
}

function Pill({ tone, title, children }: { tone: Tone; title?: string; children: ReactNode }) {
  return (
    <span
      title={title}
      className={`inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-semibold ${TONE_CLASS[tone]}`}
    >
      {children}
    </span>
  );
}

function FreshnessChip({ grade }: { grade: InspectionView["freshness_grade"] }) {
  if (grade === "UNSUPPORTED") {
    return <Pill tone="grey">Outside model coverage</Pill>;
  }
  const tone: Tone = grade === "A" ? "green" : grade === "B" ? "amber" : "red";
  return <Pill tone={tone}>Grade {grade}</Pill>;
}

function FeedbackLine({ feedback }: { feedback: Feedback }) {
  if (!feedback) return null;
  const isError = feedback.tone === "error";
  return (
    <p
      role={isError ? "alert" : "status"}
      className={`flex items-start gap-2 text-sm ${isError ? "text-red-700" : "text-emerald-700"}`}
    >
      {isError && <AlertCircle className="mt-0.5 size-4 shrink-0" />}
      <span>{feedback.text}</span>
    </p>
  );
}

function DeliveryHeader({
  delivery,
  onChanged,
}: {
  delivery: DeliverySummary;
  onChanged: () => Promise<void>;
}) {
  const [busy, setBusy] = useState<false | "inspection_complete" | "closed">(false);
  const [feedback, setFeedback] = useState<Feedback>(null);

  async function advance(next: "inspection_complete" | "closed") {
    setBusy(next);
    setFeedback(null);
    try {
      await updateDeliveryStatus(delivery.id, next);
      await onChanged();
    } catch (err) {
      setFeedback({ tone: "error", text: errorMessage(err) });
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
        <Link href="/deliveries" className="text-orange-600 hover:underline">
          ← Receiving dock
        </Link>
        <Link href={`/deliveries/${delivery.id}/trace`} className="text-orange-600 hover:underline">
          Lineage trace →
        </Link>
      </div>

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex min-w-0 flex-col gap-1">
          <h1 className="break-all font-mono text-xl font-bold text-gray-900">{delivery.id}</h1>
          <p className="text-sm text-gray-700">
            {delivery.supplier_name} · {delivery.species} · {delivery.fish_family}
          </p>
          <p className="text-sm text-gray-600">
            Stated {delivery.stated_quantity} {delivery.quantity_unit} · Truck{" "}
            {delivery.truck_identifier ?? "—"} · Received {formatTime(delivery.received_at)}
          </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <Pill tone={DELIVERY_STATUS_TONE[delivery.status]}>{STATUS_LABEL[delivery.status]}</Pill>
          {delivery.status === "active_receiving" && (
            <Button onClick={() => advance("inspection_complete")} disabled={busy !== false}>
              {busy === "inspection_complete" ? "Finishing…" : "Finish inspection"}
            </Button>
          )}
          {delivery.status === "disposition_recorded" && (
            <Button onClick={() => advance("closed")} disabled={busy !== false}>
              {busy === "closed" ? "Closing…" : "Close delivery"}
            </Button>
          )}
        </div>
      </div>

      <dl className="grid grid-cols-3 gap-3 text-center">
        <div className="rounded-md bg-gray-50 p-3">
          <dt className="text-xs text-gray-500">Inspected</dt>
          <dd className="text-lg font-bold text-gray-900">{delivery.total_inspected}</dd>
        </div>
        <div className="rounded-md bg-gray-50 p-3">
          <dt className="text-xs text-gray-500">Flagged</dt>
          <dd className="text-lg font-bold text-gray-900">{delivery.flagged_count}</dd>
        </div>
        <div className="rounded-md bg-gray-50 p-3">
          <dt className="text-xs text-gray-500">Partial</dt>
          <dd className="text-lg font-bold text-gray-900">{delivery.partial_count}</dd>
        </div>
      </dl>

      <FeedbackLine feedback={feedback} />
    </Card>
  );
}

function ConveyorPanel({
  deliveryId,
  onChanged,
}: {
  deliveryId: string;
  onChanged: () => Promise<void>;
}) {
  const [count, setCount] = useState("5");
  const [dropEvery, setDropEvery] = useState("");
  const [busy, setBusy] = useState<false | "simulate" | "capture">(false);
  const [feedback, setFeedback] = useState<Feedback>(null);

  async function onSimulate(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const n = Number(count);
    const every = dropEvery.trim() === "" ? null : Number(dropEvery);
    if (!Number.isInteger(n) || n < 1 || n > 50) {
      setFeedback({ tone: "error", text: "Count must be a whole number from 1 to 50." });
      return;
    }
    if (every !== null && (!Number.isInteger(every) || every < 2)) {
      setFeedback({ tone: "error", text: "Drop ventral every N must be a whole number of 2 or more." });
      return;
    }
    setBusy("simulate");
    setFeedback(null);
    try {
      await simulateConveyor(deliveryId, { count: n, drop_ventral_every: every });
      setFeedback({
        tone: "success",
        text: "Simulation started. It runs in the background; results appear as polling picks them up.",
      });
      await onChanged();
    } catch (err) {
      setFeedback({ tone: "error", text: errorMessage(err) });
    } finally {
      setBusy(false);
    }
  }

  async function onCapture(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    const image = data.get("image");
    if (!(image instanceof File) || image.size === 0) {
      setFeedback({ tone: "error", text: "Choose an image file to capture." });
      return;
    }
    const side = String(data.get("view_side")) as ViewSide;
    const seqRaw = String(data.get("sequence") ?? "").trim();
    const sequence = seqRaw === "" ? undefined : Number(seqRaw);
    if (sequence !== undefined && (!Number.isInteger(sequence) || sequence < 1)) {
      setFeedback({ tone: "error", text: "Sequence number must be a whole number of 1 or more." });
      return;
    }
    setBusy("capture");
    setFeedback(null);
    try {
      await captureView(deliveryId, side, image, sequence);
      form.reset();
      setFeedback({ tone: "success", text: `${side} view captured.` });
      await onChanged();
    } catch (err) {
      setFeedback({ tone: "error", text: errorMessage(err) });
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card className="flex flex-col gap-6">
      <h2 className="text-base font-semibold text-gray-900">Conveyor &amp; capture</h2>

      <form onSubmit={onSimulate} className="flex flex-wrap items-end gap-3">
        <label className={LABEL_CLASS}>
          Fish to simulate
          <input
            type="number"
            min={1}
            max={50}
            step={1}
            required
            value={count}
            onChange={(e) => setCount(e.target.value)}
            className={`${INPUT_CLASS} w-32`}
          />
        </label>
        <label className={LABEL_CLASS}>
          Drop ventral every N (optional)
          <input
            type="number"
            min={2}
            step={1}
            value={dropEvery}
            placeholder="off"
            onChange={(e) => setDropEvery(e.target.value)}
            className={`${INPUT_CLASS} w-40`}
          />
        </label>
        <Button type="submit" disabled={busy !== false}>
          {busy === "simulate" ? "Starting…" : "Simulate conveyor"}
        </Button>
      </form>

      <form onSubmit={onCapture} className="flex flex-wrap items-end gap-3 border-t border-gray-200 pt-6">
        <label className={LABEL_CLASS}>
          Image
          <input type="file" name="image" accept="image/*" required className="text-sm text-gray-700" />
        </label>
        <label className={LABEL_CLASS}>
          View
          <select name="view_side" defaultValue="dorsal" className={INPUT_CLASS}>
            <option value="dorsal">Dorsal</option>
            <option value="ventral">Ventral</option>
          </select>
        </label>
        <label className={LABEL_CLASS}>
          Sequence # (optional)
          <input
            type="number"
            name="sequence"
            min={1}
            step={1}
            placeholder="auto"
            className={`${INPUT_CLASS} w-32`}
          />
        </label>
        <Button type="submit" variant="outline" disabled={busy !== false}>
          {busy === "capture" ? "Capturing…" : "Capture view"}
        </Button>
      </form>

      <p className="text-xs text-gray-500">
        Operator-assisted capture. Pass a sequence number to pair a ventral view with a specific fish.
      </p>
      <FeedbackLine feedback={feedback} />
    </Card>
  );
}

function BoxOverlay({ defect, width, height }: { defect: Defect; width: number; height: number }) {
  const [x1, y1, x2, y2] = defect.bbox;
  return (
    <div
      className="pointer-events-none absolute border-2 border-orange-500"
      style={{
        left: `${(x1 / width) * 100}%`,
        top: `${(y1 / height) * 100}%`,
        width: `${((x2 - x1) / width) * 100}%`,
        height: `${((y2 - y1) / height) * 100}%`,
      }}
    >
      <span className="absolute left-0 top-0 whitespace-nowrap bg-orange-500 px-1 text-[10px] font-semibold text-white">
        {defect.label} {Math.round(defect.confidence * 100)}%
      </span>
    </div>
  );
}

function ViewPanel({ side, view }: { side: ViewSide; view: InspectionView }) {
  const [natural, setNatural] = useState<{ w: number; h: number } | null>(null);
  const [imageFailed, setImageFailed] = useState(false);
  const hasSize = natural !== null && natural.w > 0 && natural.h > 0;

  return (
    <figure className="flex flex-col gap-2">
      <figcaption className="text-xs font-semibold uppercase tracking-wide text-gray-500">{side} view</figcaption>
      <div className="relative overflow-hidden rounded-md bg-gray-100">
        {imageFailed ? (
          <div className="flex h-48 items-center justify-center text-sm text-gray-500">Image unavailable</div>
        ) : (
          <img
            src={getFullImageUrl(view.image_path)}
            alt={`${side} view`}
            className="block h-auto w-full"
            onLoad={(e) =>
              setNatural({ w: e.currentTarget.naturalWidth, h: e.currentTarget.naturalHeight })
            }
            onError={() => setImageFailed(true)}
          />
        )}
        {hasSize &&
          view.defects.map((defect, i) => (
            <BoxOverlay key={i} defect={defect} width={natural.w} height={natural.h} />
          ))}
      </div>
      <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs text-gray-600">
        <dt>Freshness</dt>
        <dd>
          <FreshnessChip grade={view.freshness_grade} />
        </dd>
        <dt>Confidence</dt>
        <dd>{(view.freshness_confidence * 100).toFixed(1)}%</dd>
        <dt>Defects</dt>
        <dd>{view.defects.length}</dd>
        <dt>Inference</dt>
        <dd>{INFERENCE_LABEL[view.inference_mode]}</dd>
        <dt>Latency</dt>
        <dd>{view.inference_latency_ms} ms</dd>
        <dt>SHA-256</dt>
        <dd>
          <code className="font-mono" title={view.sha256}>
            {view.sha256.slice(0, 12)}
          </code>
        </dd>
      </dl>
    </figure>
  );
}

function InspectionRow({ inspection }: { inspection: FishInspection }) {
  const [open, setOpen] = useState(false);
  const warning = MISSING_VIEW_WARNING[inspection.status];
  const viewFor = (side: ViewSide) => inspection.views.find((v) => v.view_side === side);

  return (
    <li className="rounded-md border border-gray-200">
      <button
        type="button"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
        className="flex w-full flex-wrap items-center gap-2 p-3 text-left"
      >
        <span className="font-mono text-sm font-semibold text-gray-900">#{inspection.sequence_in_delivery}</span>
        <Pill tone={INSPECTION_STATUS_TONE[inspection.status]}>{inspection.status}</Pill>
        {inspection.flagged_for_review && <Pill tone="red">Flagged</Pill>}
        {inspection.flag_reasons.map((reason) => (
          <Pill key={reason} tone="grey">
            {reason}
          </Pill>
        ))}
        {warning && (
          <span className="flex items-center gap-1 text-xs font-medium text-amber-700">
            <AlertCircle className="size-3.5" />
            {warning}
          </span>
        )}
        <span className="ml-auto text-xs text-gray-500">{open ? "Hide views" : "Show views"}</span>
      </button>

      {open && (
        <div className="grid grid-cols-1 gap-4 border-t border-gray-200 p-3 sm:grid-cols-2">
          {(["dorsal", "ventral"] as const).map((side) => {
            const view = viewFor(side);
            return view ? (
              <ViewPanel key={side} side={side} view={view} />
            ) : (
              <div
                key={side}
                className="flex min-h-40 items-center justify-center rounded-md border-2 border-dashed border-gray-300 p-4 text-sm text-gray-500"
              >
                {side === "dorsal" ? "Dorsal" : "Ventral"} view not captured
              </div>
            );
          })}
        </div>
      )}
    </li>
  );
}

function InspectionList({
  inspections,
  total,
  page,
  limit,
  onPage,
}: {
  inspections: FishInspection[];
  total: number;
  page: number;
  limit: number;
  onPage: (next: number) => void;
}) {
  const totalPages = Math.max(1, Math.ceil(total / limit));
  return (
    <Card className="flex flex-col gap-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-base font-semibold text-gray-900">Inspections</h2>
        <span className="text-xs text-gray-500">{total} total</span>
      </div>
      <p className="text-xs text-gray-500">
        AI observations for review, not decisions. Human dispositions are recorded below.
      </p>

      {inspections.length === 0 ? (
        <p className="text-sm text-gray-500">No fish captured yet.</p>
      ) : (
        <ul className="flex flex-col gap-3">
          {inspections.map((inspection) => (
            <InspectionRow key={inspection.id} inspection={inspection} />
          ))}
        </ul>
      )}

      {totalPages > 1 && (
        <nav className="flex items-center justify-between text-sm text-gray-700">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => onPage(page - 1)}>
            Previous
          </Button>
          <span>
            Page {page} of {totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            disabled={page >= totalPages}
            onClick={() => onPage(page + 1)}
          >
            Next
          </Button>
        </nav>
      )}
    </Card>
  );
}

const SWITCH_ROOM = "receiving-qc";

function SignedBadge({ via, messageId }: { via?: string | null; messageId?: string | null }) {
  if (via !== "switch_gate") {
    return (
      <Pill tone="grey" title="Recorded before Switch sign-off was required">
        Legacy entry
      </Pill>
    );
  }
  return (
    <Pill tone="sky" title={messageId ? `Switch message ${messageId}` : undefined}>
      Signed in Switch
    </Pill>
  );
}

function num(v: unknown): number {
  return typeof v === "number" ? v : Number(v ?? 0);
}

function describeProposal(p: RecordProposal): string {
  const x = p.payload;
  if (p.kind === "disposition") {
    const lot = x.output_lot_id ? ` → ${String(x.output_lot_id)}` : "";
    return `${String(x.disposition)} ${num(x.affected_quantity)} ${String(x.quantity_unit ?? "")}${lot} · "${String(
      x.decision_reason ?? ""
    )}"`;
  }
  const stage = STAGE_LABEL[x.stage as ProcessingStage] ?? String(x.stage);
  const losses = num(x.normal_yield_loss) + num(x.qc_reject_loss);
  return `${stage}: ${String(x.input_ref)} → ${String(x.output_lot_id)} · in ${num(x.quantity_in)} = out ${num(
    x.quantity_out
  )} + losses ${losses} + variance ${num(x.unexplained_variance)}`;
}

function ProposalList({
  proposals,
  kind,
  signer,
}: {
  proposals: RecordProposal[];
  kind: RecordProposal["kind"];
  signer: string;
}) {
  const mine = proposals.filter((p) => p.kind === kind);
  const pending = mine.filter((p) => p.status === "pending");
  const rejected = mine.filter((p) => p.status === "rejected");

  return (
    <div className="flex flex-col gap-3 rounded-md border border-sky-200 bg-sky-50/60 p-4">
      <div className="flex flex-col gap-1">
        <h3 className="text-sm font-semibold text-sky-900">Waiting for sign-off in Switch</h3>
        <p className="text-xs text-sky-800">
          qc-agent drafts these in the <span className="font-mono">{SWITCH_ROOM}</span> room. Nothing is recorded
          until {signer} types the command there. This page can&apos;t write records.
        </p>
      </div>
      {pending.length === 0 ? (
        <p className="text-sm text-sky-900/70">No drafts waiting.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {pending.map((p) => (
            <li key={p.id} className="flex flex-col gap-1 rounded-md border border-sky-200 bg-white p-3 text-sm">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-mono text-xs font-semibold text-gray-900">{p.id}</span>
                <Pill tone="amber">Draft</Pill>
                <span className="text-gray-700">{describeProposal(p)}</span>
              </div>
              <code className="self-start rounded bg-gray-900 px-2 py-1 font-mono text-xs text-emerald-300">
                {p.approve_command}
              </code>
            </li>
          ))}
        </ul>
      )}
      {rejected.length > 0 && (
        <ul className="flex flex-col gap-1 text-xs text-gray-600">
          {rejected.map((p) => (
            <li key={p.id}>
              <span className="font-mono">{p.id}</span> rejected by {p.decided_by ?? "?"}
              {p.decision_note ? `: "${p.decision_note}"` : ""} · {describeProposal(p)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function DispositionSection({
  delivery,
  dispositions,
  proposals,
}: {
  delivery: DeliverySummary;
  dispositions: HumanDisposition[];
  proposals: RecordProposal[];
}) {
  const open = delivery.status === "inspection_complete" || delivery.status === "disposition_recorded";
  const dispositioned = dispositions.filter((d) => !d.superseded).reduce((sum, d) => sum + d.affected_quantity, 0);

  return (
    <Card className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h2 className="text-base font-semibold text-gray-900">Disposition</h2>
        <p className="text-xs text-gray-500">
          Dispositioned {dispositioned} of {delivery.stated_quantity} {delivery.quantity_unit}. Only a QC supervisor
          can sign one, from the Switch room. A correction supersedes an earlier row, and the original stays in the
          history.
        </p>
      </div>

      {open ? (
        <ProposalList proposals={proposals} kind="disposition" signer="a QC supervisor" />
      ) : (
        <p className="text-sm text-gray-500">
          {delivery.status === "active_receiving"
            ? "Finish inspection to start recording dispositions."
            : "This delivery is closed."}
        </p>
      )}

      {dispositions.length === 0 ? (
        <p className="text-sm text-gray-500">No dispositions recorded yet.</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {dispositions.map((d) => (
            <li
              key={d.id}
              className={`rounded-md border border-gray-200 p-3 text-sm ${d.superseded ? "opacity-50" : ""}`}
            >
              <div className="flex flex-wrap items-center gap-2">
                <Pill tone={OUTCOME_TONE[d.disposition]}>{d.disposition}</Pill>
                <span className="font-medium text-gray-900">
                  {d.affected_quantity} {d.quantity_unit}
                </span>
                <span className="text-gray-600">Lot {d.output_lot_id ?? "—"}</span>
                {d.supersedes_id !== null && (
                  <span className="text-xs text-gray-500">corrects #{d.supersedes_id}</span>
                )}
                {d.superseded && <Pill tone="grey">Superseded by correction</Pill>}
                <SignedBadge via={d.authorized_via} messageId={d.switch_message_id} />
              </div>
              <p className="mt-1 text-gray-700">{d.decision_reason}</p>
              <p className="mt-1 text-xs text-gray-500">
                #{d.id} · signed by <span className="font-medium text-gray-700">{d.authorized_by}</span> ·{" "}
                {formatTime(d.decided_at)}
                {d.switch_message_id && <span className="font-mono"> · {d.switch_message_id}</span>}
              </p>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

function MovementSection({
  delivery,
  movements,
  proposals,
}: {
  delivery: DeliverySummary;
  movements: MaterialMovement[];
  proposals: RecordProposal[];
}) {
  const open = delivery.status === "disposition_recorded";

  return (
    <Card className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h2 className="text-base font-semibold text-gray-900">Movements</h2>
        <p className="text-xs text-gray-500">
          Quantity in must equal quantity out plus losses and variance. Unit: {delivery.quantity_unit}. A floor
          operator or the QC supervisor confirms each one from the Switch room.
        </p>
      </div>

      {open ? (
        <ProposalList proposals={proposals} kind="movement" signer="a floor operator or the QC supervisor" />
      ) : (
        <p className="text-sm text-gray-500">
          Movements open once dispositions are recorded and the delivery is in disposition recorded status.
        </p>
      )}

      {movements.length === 0 ? (
        <p className="text-sm text-gray-500">No movements recorded yet.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px] text-left text-sm">
            <thead className="text-xs uppercase text-gray-500">
              <tr>
                <th scope="col" className="py-2 pr-3 font-semibold">Stage</th>
                <th scope="col" className="pr-3 font-semibold">Input → output</th>
                <th scope="col" className="pr-3 font-semibold">In</th>
                <th scope="col" className="pr-3 font-semibold">Out</th>
                <th scope="col" className="pr-3 font-semibold">Losses (normal / QC)</th>
                <th scope="col" className="pr-3 font-semibold">Variance</th>
                <th scope="col" className="pr-3 font-semibold">Signed by</th>
                <th scope="col" className="font-semibold">Time</th>
              </tr>
            </thead>
            <tbody>
              {movements.map((m) => (
                <tr key={m.id} className="border-t border-gray-200 align-top">
                  <td className="py-2 pr-3">{STAGE_LABEL[m.stage]}</td>
                  <td className="pr-3 font-mono text-xs">
                    {m.input_ref} → {m.output_lot_id}
                  </td>
                  <td className="pr-3">{m.quantity_in}</td>
                  <td className="pr-3">{m.quantity_out}</td>
                  <td className="pr-3">
                    {m.normal_yield_loss} / {m.qc_reject_loss}
                  </td>
                  <td className="pr-3">{m.unexplained_variance}</td>
                  <td className="pr-3">
                    <div className="flex flex-col items-start gap-1">
                      <span>{m.operator_id}</span>
                      <SignedBadge via={m.authorized_via} messageId={m.switch_message_id} />
                    </div>
                  </td>
                  <td className="whitespace-nowrap text-xs">{formatTime(m.timestamp)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}

export default function DeliveryQcWorkspacePage() {
  const { id: deliveryId } = useParams<{ id: string }>();
  const [detail, setDetail] = useState<DeliveryDetail | null>(null);
  const [page, setPage] = useState(1);
  const [refreshToken, setRefreshToken] = useState(0);
  const [loadError, setLoadError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setRefreshToken((t) => t + 1);
  }, []);

  useEffect(() => {
    let ignore = false;
    getDeliveryById(deliveryId, { page, limit: 25 })
      .then((data) => {
        if (ignore) return;
        setDetail(data);
        setLoadError(null);
      })
      .catch((err: unknown) => {
        if (!ignore) setLoadError(errorMessage(err));
      });
    return () => {
      ignore = true;
    };
  }, [deliveryId, page, refreshToken]);

  const status = detail?.delivery.status;
  useEffect(() => {
    if (status !== "active_receiving") return;
    const timer = setInterval(() => void refresh(), POLL_MS);
    return () => clearInterval(timer);
  }, [status, refresh]);

  // Records are signed in the Switch room, so watch the drafts and reload when one is decided there.
  const [proposals, setProposals] = useState<RecordProposal[]>([]);
  const signingOpen = status === "inspection_complete" || status === "disposition_recorded";
  useEffect(() => {
    if (!signingOpen) return;
    let ignore = false;
    let decided: string | null = null;
    const load = () =>
      getProposals(deliveryId)
        .then((rows) => {
          if (ignore) return;
          setProposals(rows);
          const key = rows.filter((p) => p.status !== "pending").map((p) => p.id).join(",");
          if (decided !== null && key !== decided) void refresh();
          decided = key;
        })
        .catch(() => undefined);
    void load();
    const timer = setInterval(load, POLL_MS);
    return () => {
      ignore = true;
      clearInterval(timer);
    };
  }, [deliveryId, signingOpen, refresh]);

  if (!detail) {
    const loading = loadError === null;
    return (
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 p-6">
        {loading ? (
          <p className="flex items-center gap-2 text-sm text-gray-600">
            <Loader2 className="size-4 animate-spin" />
            Loading delivery…
          </p>
        ) : (
          <Card className="flex flex-col gap-4">
            <FeedbackLine feedback={{ tone: "error", text: loadError ?? "Delivery could not be loaded." }} />
            <div className="flex flex-wrap gap-3 text-sm">
              <Button variant="outline" onClick={() => void refresh()}>
                Retry
              </Button>
              <Link href="/deliveries" className="self-center text-orange-600 hover:underline">
                ← Receiving dock
              </Link>
            </div>
          </Card>
        )}
      </div>
    );
  }

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 p-6">
      <DeliveryHeader delivery={detail.delivery} onChanged={refresh} />
      {loadError && <FeedbackLine feedback={{ tone: "error", text: `Refresh failed: ${loadError}` }} />}
      {detail.delivery.status === "active_receiving" && (
        <ConveyorPanel deliveryId={detail.delivery.id} onChanged={refresh} />
      )}
      <InspectionList
        inspections={detail.inspections}
        total={detail.inspections_total}
        page={page}
        limit={detail.limit}
        onPage={setPage}
      />
      <DispositionSection
        delivery={detail.delivery}
        dispositions={detail.dispositions}
        proposals={proposals}
      />
      <MovementSection delivery={detail.delivery} movements={detail.movements} proposals={proposals} />
    </div>
  );
}
