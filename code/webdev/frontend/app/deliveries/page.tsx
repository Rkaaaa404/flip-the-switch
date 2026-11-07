"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Loader2, AlertCircle, CheckCircle2 } from "lucide-react";
import { createDelivery, getDeliveries } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import type {
  DeliveryCreate,
  DeliveryListResponse,
  DeliveryStatus,
  QuantityUnit,
} from "@/types/delivery";

const FISH_FAMILIES = ["Scombridae", "Cichlidae", "Salmonidae", "Other"];
const POLL_INTERVAL_MS = 5000;

const STATUS_STYLES: Record<DeliveryStatus, string> = {
  active_receiving: "bg-sky-100 text-sky-800 border-sky-200",
  inspection_complete: "bg-amber-100 text-amber-800 border-amber-200",
  disposition_recorded: "bg-emerald-100 text-emerald-800 border-emerald-200",
  closed: "bg-slate-100 text-slate-700 border-slate-200",
};

const INPUT_CLASS =
  "w-full px-3 py-2 text-sm font-sans text-zinc-900 bg-white rounded-md border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-400";

const humanize = (value: string) => {
  const text = value.replace(/_/g, " ").toLowerCase();
  return text.charAt(0).toUpperCase() + text.slice(1);
};

const formatQuantity = (value: number) =>
  value.toLocaleString(undefined, { maximumFractionDigits: 2 });

type IntakeForm = {
  supplier_name: string;
  species: string;
  fish_family: string;
  stated_quantity: string;
  quantity_unit: QuantityUnit;
  truck_identifier: string;
  created_by: string;
};

const EMPTY_FORM: IntakeForm = {
  supplier_name: "",
  species: "",
  fish_family: FISH_FAMILIES[0],
  stated_quantity: "",
  quantity_unit: "kg",
  truck_identifier: "",
  created_by: "",
};

export default function DeliveriesPage() {
  const [list, setList] = useState<DeliveryListResponse | null>(null);
  const [listError, setListError] = useState<string | null>(null);
  const [isListLoading, setIsListLoading] = useState<boolean>(true);

  const [form, setForm] = useState<IntakeForm>(EMPTY_FORM);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [createdId, setCreatedId] = useState<string | null>(null);

  const [refreshKey, setRefreshKey] = useState<number>(0);

  const hasActiveReceiving =
    list?.items.some((item) => item.status === "active_receiving") ?? false;

  // Loads the list on mount and after each intake (refreshKey). While any delivery is
  // still receiving, the same load repeats on an interval; the interval stops once none are active.
  useEffect(() => {
    let cancelled = false;
    const load = () => {
      getDeliveries({ limit: 50 })
        .then((data) => {
          if (!cancelled) {
            setList(data);
            setListError(null);
          }
        })
        .catch((err) => {
          if (!cancelled) {
            setListError(err instanceof Error ? err.message : "Failed to load deliveries.");
          }
        })
        .finally(() => {
          if (!cancelled) setIsListLoading(false);
        });
    };

    load();
    if (!hasActiveReceiving) {
      return () => {
        cancelled = true;
      };
    }
    const timer = setInterval(load, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [hasActiveReceiving, refreshKey]);

  const updateField = <K extends keyof IntakeForm>(key: K, value: IntakeForm[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const quantity = Number(form.stated_quantity);
    if (!(quantity > 0)) {
      setFormError("Stated quantity must be greater than 0.");
      return;
    }

    const body: DeliveryCreate = {
      supplier_name: form.supplier_name.trim(),
      species: form.species.trim(),
      fish_family: form.fish_family,
      stated_quantity: quantity,
      quantity_unit: form.quantity_unit,
      truck_identifier: form.truck_identifier.trim() || null,
      created_by: form.created_by.trim(),
    };

    setIsSubmitting(true);
    setFormError(null);
    setCreatedId(null);
    try {
      const created = await createDelivery(body);
      setForm(EMPTY_FORM);
      setCreatedId(created.id);
      setRefreshKey((key) => key + 1);
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Failed to create delivery.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const items = list?.items ?? [];

  return (
    <div className="flex flex-col gap-6 p-6 max-w-7xl mx-auto w-full">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-black font-sans text-zinc-900">Receiving &amp; Trace</h1>
        <p className="text-sm font-sans text-slate-600">
          Each supplier delivery is inspected from dorsal and ventral views, then traced
          through dispositions and material movements down to storage and dispatch.
        </p>
      </header>

      {/* Intake Form */}
      <Card className="p-5 flex flex-col gap-4">
        <div className="flex flex-col gap-1">
          <h2 className="text-base font-bold font-sans text-zinc-900">New supplier delivery</h2>
          <p className="text-xs font-sans text-slate-500">
            Record the intake before inspecting fish. The stated quantity is the supplier&apos;s claim
            and is reconciled against dispositions later.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
            Supplier name
            <input
              required
              className={INPUT_CLASS}
              value={form.supplier_name}
              disabled={isSubmitting}
              onChange={(e) => updateField("supplier_name", e.target.value)}
            />
          </label>

          <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
            Species
            <input
              required
              className={INPUT_CLASS}
              value={form.species}
              disabled={isSubmitting}
              onChange={(e) => updateField("species", e.target.value)}
            />
          </label>

          <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
            Fish family
            <select
              className={INPUT_CLASS}
              value={form.fish_family}
              disabled={isSubmitting}
              onChange={(e) => updateField("fish_family", e.target.value)}
            >
              {FISH_FAMILIES.map((family) => (
                <option key={family} value={family}>
                  {family}
                </option>
              ))}
            </select>
            {form.fish_family === "Other" && (
              <span className="font-normal text-amber-700">
                Outside model coverage. Inspections will be recorded as UNSUPPORTED evidence.
              </span>
            )}
          </label>

          <div className="grid grid-cols-2 gap-3">
            <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
              Stated quantity
              <input
                required
                type="number"
                min="0"
                step="any"
                className={INPUT_CLASS}
                value={form.stated_quantity}
                disabled={isSubmitting}
                onChange={(e) => updateField("stated_quantity", e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
              Unit
              <select
                className={INPUT_CLASS}
                value={form.quantity_unit}
                disabled={isSubmitting}
                onChange={(e) => updateField("quantity_unit", e.target.value as QuantityUnit)}
              >
                <option value="kg">kg</option>
                <option value="count">count</option>
              </select>
            </label>
          </div>

          <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
            Truck identifier <span className="font-normal text-slate-400">(optional)</span>
            <input
              className={INPUT_CLASS}
              value={form.truck_identifier}
              disabled={isSubmitting}
              onChange={(e) => updateField("truck_identifier", e.target.value)}
            />
          </label>

          <label className="flex flex-col gap-1 text-xs font-semibold font-sans text-slate-600">
            Operator ID
            <input
              required
              className={INPUT_CLASS}
              value={form.created_by}
              disabled={isSubmitting}
              onChange={(e) => updateField("created_by", e.target.value)}
            />
          </label>

          <div className="md:col-span-2 lg:col-span-3 flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-col gap-1 text-sm font-sans min-h-[1.25rem]">
              {formError && (
                <span className="flex items-center gap-1.5 text-rose-700">
                  <AlertCircle className="size-4 shrink-0" />
                  {formError}
                </span>
              )}
              {createdId && (
                <span className="flex items-center gap-1.5 text-emerald-700">
                  <CheckCircle2 className="size-4 shrink-0" />
                  Delivery created:{" "}
                  <Link href={`/deliveries/${createdId}`} className="font-mono font-bold underline">
                    {createdId}
                  </Link>
                </span>
              )}
            </div>
            <Button type="submit" variant="primary" disabled={isSubmitting}>
              {isSubmitting && <Loader2 className="animate-spin" />}
              {isSubmitting ? "Creating..." : "Create delivery"}
            </Button>
          </div>
        </form>
      </Card>

      {/* Deliveries Table */}
      <Card className="p-0 flex flex-col">
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
          <h2 className="text-base font-bold font-sans text-zinc-900">Deliveries</h2>
          <span className="text-xs font-sans text-slate-500">
            {hasActiveReceiving ? "Live: refreshing every 5 s" : `${items.length} shown`}
          </span>
        </div>

        {listError && (
          <div className="m-5 p-3 rounded-md border border-rose-300 bg-rose-50 text-sm font-sans text-rose-800 flex items-center gap-2">
            <AlertCircle className="size-4 shrink-0" />
            <span>{listError}</span>
          </div>
        )}

        {isListLoading ? (
          <div className="py-12 flex items-center justify-center gap-2 text-slate-400">
            <Loader2 className="size-5 animate-spin text-sky-600" />
            <span className="text-xs font-sans">Loading deliveries...</span>
          </div>
        ) : items.length === 0 ? (
          !listError && (
            <div className="py-12 text-center text-sm font-sans text-slate-500">
              No deliveries yet. Create one above to start receiving.
            </div>
          )
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm font-sans text-left">
              <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wide">
                <tr>
                  <th className="px-4 py-2.5">ID</th>
                  <th className="px-4 py-2.5">Supplier</th>
                  <th className="px-4 py-2.5">Species</th>
                  <th className="px-4 py-2.5">Received</th>
                  <th className="px-4 py-2.5">Stated</th>
                  <th className="px-4 py-2.5">Status</th>
                  <th className="px-4 py-2.5 text-right">Inspected</th>
                  <th className="px-4 py-2.5 text-right">Flagged</th>
                  <th className="px-4 py-2.5 text-right">Partial</th>
                  <th className="px-4 py-2.5"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/70">
                    <td className="px-4 py-2.5 font-mono text-xs font-bold">
                      <Link href={`/deliveries/${item.id}`} className="text-sky-700 hover:underline">
                        {item.id}
                      </Link>
                    </td>
                    <td className="px-4 py-2.5 text-zinc-900">{item.supplier_name}</td>
                    <td className="px-4 py-2.5 text-slate-700">{item.species}</td>
                    <td className="px-4 py-2.5 text-slate-600 whitespace-nowrap">
                      {new Date(item.received_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-2.5 font-mono text-xs text-slate-700 whitespace-nowrap">
                      {formatQuantity(item.stated_quantity)} {item.quantity_unit}
                    </td>
                    <td className="px-4 py-2.5">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-full border text-xs font-bold whitespace-nowrap ${STATUS_STYLES[item.status]}`}
                      >
                        {humanize(item.status)}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 text-right font-mono">{item.total_inspected}</td>
                    <td
                      className={`px-4 py-2.5 text-right font-mono font-bold ${
                        item.flagged_count > 0 ? "text-red-600" : "text-slate-400"
                      }`}
                    >
                      {item.flagged_count}
                    </td>
                    <td
                      className={`px-4 py-2.5 text-right font-mono font-bold ${
                        item.partial_count > 0 ? "text-amber-600" : "text-slate-400"
                      }`}
                    >
                      {item.partial_count}
                    </td>
                    <td className="px-4 py-2.5 text-right">
                      <Link
                        href={`/deliveries/${item.id}/trace`}
                        className="text-xs font-bold text-sky-700 hover:text-sky-900 hover:underline"
                      >
                        Trace
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
