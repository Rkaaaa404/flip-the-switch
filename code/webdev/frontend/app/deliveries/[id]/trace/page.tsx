"use client";

import React, { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { AlertCircle, ArrowRight, CheckCircle2, Loader2, Search } from "lucide-react";
import { getDeliveryTrace, getLotProvenance } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type {
  DeliveryStatus,
  DispositionOutcome,
  DeliveryTraceTree,
  LotProvenance,
  MovementNode,
  MissingLink,
  HumanDisposition,
  QuantityUnit,
} from "@/types/delivery";

const STATUS_STYLES: Record<DeliveryStatus, string> = {
  active_receiving: "bg-sky-100 text-sky-800 border-sky-200",
  inspection_complete: "bg-amber-100 text-amber-800 border-amber-200",
  disposition_recorded: "bg-emerald-100 text-emerald-800 border-emerald-200",
  closed: "bg-slate-100 text-slate-700 border-slate-200",
};

const OUTCOME_STYLES: Record<DispositionOutcome, string> = {
  ACCEPT: "bg-emerald-100 text-emerald-800 border-emerald-200",
  REJECT: "bg-red-100 text-red-800 border-red-200",
  REPROCESS: "bg-amber-100 text-amber-800 border-amber-200",
  DOWNGRADE: "bg-violet-100 text-violet-800 border-violet-200",
};

const INPUT_CLASS =
  "flex-1 min-w-0 px-3 py-2 text-sm font-mono text-zinc-900 bg-white rounded-md border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500";

const humanize = (value: string) => {
  const text = value.replace(/_/g, " ").toLowerCase();
  return text.charAt(0).toUpperCase() + text.slice(1);
};

const formatQuantity = (value: number, unit: QuantityUnit) =>
  `${value.toLocaleString(undefined, { maximumFractionDigits: 2 })} ${unit}`;

const errorMessage = (err: unknown, fallback: string) =>
  err instanceof Error ? err.message : fallback;

type LineageNode = { movement: MovementNode; children: LineageNode[] };

/**
 * Builds the lineage forest from the flat movement list. Roots are movements whose
 * input_ref is the delivery id. Each movement is attached at most once, so cycles in
 * the data cannot cause unbounded recursion. Movements never reached are returned as unlinked.
 */
function buildLineage(trace: DeliveryTraceTree): { roots: LineageNode[]; unlinked: MovementNode[] } {
  const byInput = new Map<string, MovementNode[]>();
  for (const movement of trace.movements) {
    const bucket = byInput.get(movement.input_ref) ?? [];
    bucket.push(movement);
    byInput.set(movement.input_ref, bucket);
  }

  const visited = new Set<number>();
  const attach = (ref: string): LineageNode[] =>
    (byInput.get(ref) ?? [])
      .filter((movement) => !visited.has(movement.id))
      .map((movement) => {
        visited.add(movement.id);
        return { movement, children: attach(movement.output_lot_id) };
      });

  const roots = attach(trace.delivery.id);
  const unlinked = trace.movements.filter((movement) => !visited.has(movement.id));
  return { roots, unlinked };
}

export default function LineageTracePage() {
  const params = useParams<{ id: string }>();
  const id = params.id;

  const [trace, setTrace] = useState<DeliveryTraceTree | null>(null);
  const [traceError, setTraceError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const [lotInput, setLotInput] = useState<string>("");
  const [provenance, setProvenance] = useState<LotProvenance | null>(null);
  const [provenanceError, setProvenanceError] = useState<string | null>(null);
  const [isLookingUp, setIsLookingUp] = useState<boolean>(false);

  useEffect(() => {
    let cancelled = false;
    getDeliveryTrace(id)
      .then((data) => {
        if (!cancelled) {
          setTrace(data);
          setTraceError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) setTraceError(errorMessage(err, "Failed to load trace."));
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  const lineage = useMemo(() => (trace ? buildLineage(trace) : null), [trace]);

  const handleLookup = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const lotId = lotInput.trim();
    if (!lotId) return;

    setIsLookingUp(true);
    setProvenanceError(null);
    try {
      setProvenance(await getLotProvenance(lotId));
    } catch (err) {
      setProvenance(null);
      setProvenanceError(errorMessage(err, "Failed to look up lot provenance."));
    } finally {
      setIsLookingUp(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center gap-2 p-12 text-slate-400">
        <Loader2 className="size-6 animate-spin text-sky-600" />
        <span className="text-sm font-sans">Loading lineage...</span>
      </div>
    );
  }

  if (traceError || !trace || !lineage) {
    return (
      <div className="flex flex-col gap-4 p-6 max-w-7xl mx-auto w-full">
        <Link href={`/deliveries/${id}`} className="text-sm font-bold font-sans text-sky-700 hover:underline">
          ← Back to delivery
        </Link>
        <div className="p-4 rounded-md border border-rose-300 bg-rose-50 text-sm font-sans text-rose-800 flex items-center gap-2">
          <AlertCircle className="size-4 shrink-0" />
          <span>{traceError ?? "Trace not found."}</span>
        </div>
      </div>
    );
  }

  const { delivery, inspection_summary: summary, balance, missing_links: gaps } = trace;
  const unit = delivery.quantity_unit;

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      {/* Header */}
      <header className="flex flex-col gap-2">
        <Link href={`/deliveries/${delivery.id}`} className="text-sm font-bold font-sans text-sky-700 hover:underline w-fit">
          ← Back to delivery
        </Link>
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-black font-sans text-zinc-900">Lineage Trace</h1>
          <span className="font-mono text-sm font-bold text-slate-600">{delivery.id}</span>
          <span
            className={`inline-block px-2 py-0.5 rounded-full border text-xs font-bold ${STATUS_STYLES[delivery.status]}`}
          >
            {humanize(delivery.status)}
          </span>
        </div>
        <p className="text-sm font-sans text-slate-600">
          {delivery.supplier_name} · {delivery.species} · received{" "}
          {new Date(delivery.received_at).toLocaleString()}
        </p>
      </header>

      {/* Gaps */}
      {gaps.length > 0 ? (
        <Card className="p-5 border-2 border-red-400 flex flex-col gap-3">
          <h2 className="text-base font-bold font-sans text-red-700 flex items-center gap-2">
            <AlertCircle className="size-5" />
            Unresolved gaps ({gaps.length})
          </h2>
          <ul className="flex flex-col gap-2">
            {gaps.map((gap: MissingLink, index) => (
              <li
                key={`${gap.kind}-${gap.ref}-${index}`}
                className="p-3 rounded-md bg-red-50 border border-red-200 flex flex-col gap-1 text-sm font-sans"
              >
                <span className="font-bold text-red-800">{humanize(gap.kind)}</span>
                <span className="font-mono text-xs text-red-700 break-all">{gap.ref}</span>
                <span className="text-slate-700">{gap.detail}</span>
              </li>
            ))}
          </ul>
        </Card>
      ) : (
        <div className="p-4 rounded-md border border-emerald-300 bg-emerald-50 text-sm font-sans font-semibold text-emerald-800 flex items-center gap-2">
          <CheckCircle2 className="size-4 shrink-0" />
          No gaps detected in recorded links.
        </div>
      )}

      {/* Summary Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 flex flex-col gap-3">
          <h2 className="text-base font-bold font-sans text-zinc-900">Inspections</h2>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            <Stat label="Total" value={summary.total} className="text-zinc-900" />
            <Stat label="Complete" value={summary.complete} className="text-emerald-600" />
            <Stat label="Partial dorsal" value={summary.partial_dorsal_only} className={summary.partial_dorsal_only > 0 ? "text-amber-600" : "text-slate-400"} />
            <Stat label="Partial ventral" value={summary.partial_ventral_only} className={summary.partial_ventral_only > 0 ? "text-amber-600" : "text-slate-400"} />
            <Stat label="Flagged" value={summary.flagged} className={summary.flagged > 0 ? "text-red-600" : "text-slate-400"} />
          </div>
        </Card>

        <Card
          className={`p-5 flex flex-col gap-3 ${balance.unallocated_quantity > 0 ? "border-2 border-amber-400" : ""}`}
        >
          <h2 className="text-base font-bold font-sans text-zinc-900">Quantity balance</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <Stat label="Stated" value={formatQuantity(balance.stated_quantity, balance.quantity_unit)} className="text-zinc-900" small />
            <Stat label="Dispositioned" value={formatQuantity(balance.dispositioned_quantity, balance.quantity_unit)} className="text-zinc-900" small />
            <Stat label="Allocated from intake" value={formatQuantity(balance.allocated_from_intake, balance.quantity_unit)} className="text-zinc-900" small />
            <Stat
              label="Unallocated"
              value={formatQuantity(balance.unallocated_quantity, balance.quantity_unit)}
              className={balance.unallocated_quantity > 0 ? "text-amber-600" : "text-zinc-900"}
              small
            />
          </div>
        </Card>
      </div>

      {/* Dispositions */}
      <Card className="p-5 flex flex-col gap-3">
        <h2 className="text-base font-bold font-sans text-zinc-900">
          Dispositions ({trace.dispositions.length})
        </h2>
        {trace.dispositions.length === 0 ? (
          <p className="text-sm font-sans text-slate-500">No dispositions recorded.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {trace.dispositions.map((disposition) => (
              <DispositionRow key={disposition.id} disposition={disposition} />
            ))}
          </ul>
        )}
      </Card>

      {/* Lineage Tree */}
      <Card className="p-5 flex flex-col gap-3">
        <h2 className="text-base font-bold font-sans text-zinc-900">Lineage</h2>
        <div className="p-3 rounded-md bg-sky-50 border border-sky-200 w-fit">
          <span className="font-mono text-xs font-bold text-sky-800">{delivery.id}</span>
          <span className="ml-2 text-xs font-sans text-slate-600">
            intake · {formatQuantity(delivery.stated_quantity, unit)}
          </span>
        </div>
        {lineage.roots.length === 0 ? (
          <p className="text-sm font-sans text-slate-500">No movements recorded from this delivery.</p>
        ) : (
          <LineageList nodes={lineage.roots} />
        )}

        {lineage.unlinked.length > 0 && (
          <div className="mt-4 flex flex-col gap-3">
            <h3 className="text-sm font-bold font-sans text-amber-700">
              Unlinked movements ({lineage.unlinked.length})
            </h3>
            {lineage.unlinked.map((movement) => (
              <MovementCard key={movement.id} movement={movement} />
            ))}
          </div>
        )}
      </Card>

      {/* Lot Provenance Lookup */}
      <Card className="p-5 flex flex-col gap-4">
        <div className="flex flex-col gap-1">
          <h2 className="text-base font-bold font-sans text-zinc-900">Lot provenance lookup</h2>
          <p className="text-xs font-sans text-slate-500">
            Trace any output lot back to its source delivery.
          </p>
        </div>

        <form onSubmit={handleLookup} className="flex flex-wrap items-center gap-2">
          <input
            className={INPUT_CLASS}
            placeholder="Lot ID"
            value={lotInput}
            disabled={isLookingUp}
            onChange={(e) => setLotInput(e.target.value)}
          />
          <Button type="submit" variant="outline-sky" disabled={isLookingUp || !lotInput.trim()}>
            {isLookingUp ? <Loader2 className="animate-spin" /> : <Search />}
            Look up
          </Button>
        </form>

        {provenanceError && (
          <div className="p-3 rounded-md border border-rose-300 bg-rose-50 text-sm font-sans text-rose-800 flex items-center gap-2">
            <AlertCircle className="size-4 shrink-0" />
            <span>{provenanceError}</span>
          </div>
        )}

        {provenance && <ProvenanceResult provenance={provenance} />}
      </Card>
    </div>
  );
}

function Stat({
  label,
  value,
  className,
  small = false,
}: {
  label: string;
  value: number | string;
  className: string;
  small?: boolean;
}) {
  return (
    <div className="p-3 rounded-md bg-slate-50 border border-slate-200 flex flex-col gap-1">
      <span className="text-xs font-semibold font-sans text-slate-500">{label}</span>
      <span className={`font-mono font-black ${small ? "text-sm" : "text-xl"} ${className}`}>{value}</span>
    </div>
  );
}

function DispositionRow({ disposition }: { disposition: HumanDisposition }) {
  return (
    <li
      className={`p-3 rounded-md border border-slate-200 flex flex-col gap-2 text-sm font-sans ${
        disposition.superseded ? "opacity-50" : ""
      }`}
    >
      <div className="flex flex-wrap items-center gap-2">
        <span className={`inline-block px-2 py-0.5 rounded-full border text-xs font-bold ${OUTCOME_STYLES[disposition.disposition]}`}>
          {disposition.disposition}
        </span>
        <span className={`font-mono font-bold ${disposition.superseded ? "line-through" : ""}`}>
          {formatQuantity(disposition.affected_quantity, disposition.quantity_unit)}
        </span>
        {disposition.output_lot_id && (
          <span className="font-mono text-xs text-slate-600">→ {disposition.output_lot_id}</span>
        )}
        {disposition.superseded && (
          <span className="px-2 py-0.5 rounded-sm bg-slate-200 text-slate-700 text-xs font-bold">superseded</span>
        )}
      </div>
      <div className={`text-xs text-slate-600 ${disposition.superseded ? "line-through" : ""}`}>
        {disposition.authorized_by} · {new Date(disposition.decided_at).toLocaleString()}
      </div>
      <div className={`text-slate-700 ${disposition.superseded ? "line-through" : ""}`}>
        {disposition.decision_reason}
      </div>
    </li>
  );
}

function LineageList({ nodes }: { nodes: LineageNode[] }) {
  return (
    <ul className="ml-3 border-l-2 border-slate-300 pl-4 flex flex-col gap-3">
      {nodes.map((node) => (
        <li key={node.movement.id} className="flex flex-col gap-3">
          <MovementCard movement={node.movement} />
          {node.children.length > 0 && <LineageList nodes={node.children} />}
        </li>
      ))}
    </ul>
  );
}

function MovementCard({ movement }: { movement: MovementNode }) {
  const losses = [
    { label: "Normal yield loss", value: movement.normal_yield_loss },
    { label: "QC reject loss", value: movement.qc_reject_loss },
    { label: "Unexplained variance", value: movement.unexplained_variance },
  ].filter((loss) => loss.value !== 0);

  return (
    <div className="p-3 rounded-md bg-white border border-slate-200 shadow-xs flex flex-col gap-2 text-sm font-sans">
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-bold text-zinc-900">{humanize(movement.stage)}</span>
        <span className="font-mono text-xs font-bold text-sky-700">{movement.output_lot_id}</span>
      </div>
      <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-slate-700">
        <span>{formatQuantity(movement.quantity_in, movement.quantity_unit)}</span>
        <ArrowRight className="size-3 text-slate-400" />
        <span>{formatQuantity(movement.quantity_out, movement.quantity_unit)}</span>
      </div>
      {losses.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {losses.map((loss) => (
            <span key={loss.label} className="px-2 py-0.5 rounded-sm bg-amber-50 border border-amber-200 text-xs font-mono text-amber-800">
              {loss.label}: {formatQuantity(loss.value, movement.quantity_unit)}
            </span>
          ))}
        </div>
      )}
      {(movement.storage_slots.length > 0 || movement.dispatches.length > 0) && (
        <div className="flex flex-wrap gap-2">
          {movement.storage_slots.map((slot) => (
            <span key={slot.slot_id} className="px-2 py-0.5 rounded-sm bg-indigo-50 border border-indigo-200 text-xs font-mono text-indigo-800">
              {slot.slot_id} · {slot.zone}
            </span>
          ))}
          {movement.dispatches.map((dispatch) => (
            <span key={dispatch.dispatch_id} className="px-2 py-0.5 rounded-sm bg-emerald-50 border border-emerald-200 text-xs font-sans text-emerald-800">
              <span className="font-mono">{dispatch.dispatch_id}</span> → {dispatch.buyer_name}, {dispatch.destination} ({dispatch.status})
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function ProvenanceResult({ provenance }: { provenance: LotProvenance }) {
  return (
    <div className="flex flex-col gap-4 text-sm font-sans">
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-mono font-bold text-zinc-900">{provenance.lot_id}</span>
        {provenance.delivery ? (
          <Link href={`/deliveries/${provenance.delivery.id}`} className="font-mono text-xs font-bold text-sky-700 hover:underline">
            source delivery: {provenance.delivery.id}
          </Link>
        ) : (
          <span className="text-xs text-slate-500">No source delivery linked.</span>
        )}
      </div>

      {provenance.chain.length > 0 ? (
        <div className="flex flex-wrap items-center gap-2">
          {provenance.chain.map((movement, index) => (
            <React.Fragment key={movement.id}>
              {index > 0 && <ArrowRight className="size-4 text-slate-400" />}
              <div className="p-2 rounded-md bg-slate-50 border border-slate-200 flex flex-col gap-0.5">
                <span className="font-mono text-xs text-slate-600">{movement.input_ref}</span>
                <span className="font-mono text-xs font-bold text-sky-700">→ {movement.output_lot_id}</span>
                <span className="text-[11px] text-slate-500">{humanize(movement.stage)}</span>
              </div>
            </React.Fragment>
          ))}
        </div>
      ) : (
        <p className="text-slate-500">No upstream movements in the chain.</p>
      )}

      {provenance.missing_links.length > 0 && (
        <ul className="flex flex-col gap-2">
          {provenance.missing_links.map((gap, index) => (
            <li
              key={`${gap.kind}-${gap.ref}-${index}`}
              className="p-3 rounded-md bg-red-50 border border-red-200 flex flex-col gap-1 text-sm font-sans"
            >
              <span className="font-bold text-red-800">{humanize(gap.kind)}</span>
              <span className="font-mono text-xs text-red-700 break-all">{gap.ref}</span>
              <span className="text-slate-700">{gap.detail}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
