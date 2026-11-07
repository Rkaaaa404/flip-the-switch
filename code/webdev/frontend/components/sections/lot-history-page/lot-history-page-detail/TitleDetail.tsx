"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft, Trash2, AlertTriangle, Loader2 } from "lucide-react";
import { deleteLot } from "@/lib/api";

type TitleDetailProps = {
  lotId: string;
};

export const TitleDetail = ({ lotId }: TitleDetailProps) => {
  const router = useRouter();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleDelete = async () => {
    setIsDeleting(true);
    setErrorMsg(null);
    try {
      await deleteLot(lotId);
      setIsModalOpen(false);
      router.push("/history");
      router.refresh();
    } catch (err: any) {
      setErrorMsg(err?.message || "Gagal menghapus rekaman lot.");
      setIsDeleting(false);
    }
  };

  return (
    <>
      <div className="w-full flex flex-col gap-3">
        <Link
          href="/history"
          className="inline-flex self-start items-center gap-1.5 text-xs font-bold font-sans text-sky-600 hover:text-sky-800 transition-colors"
        >
          <ArrowLeft className="size-3.5" />
          <span>Kembali ke Lot History</span>
        </Link>

        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-col">
            <h1 className="text-2xl font-black font-sans text-zinc-900 tracking-tight">
              Inspection Detail
            </h1>
            <p className="text-sm font-bold font-mono text-sky-700 mt-0.5">
              {lotId}
            </p>
          </div>

          <button
            type="button"
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-300 rounded-sm font-bold text-xs font-sans transition-colors cursor-pointer shadow-xs"
          >
            <Trash2 className="size-4 text-rose-600" />
            <span>Hapus Rekaman Lot</span>
          </button>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6 flex flex-col gap-4 border border-slate-200 animate-in zoom-in-95 duration-200">
            <div className="flex items-center gap-3 text-rose-600">
              <div className="size-10 rounded-full bg-rose-100 flex items-center justify-center shrink-0">
                <AlertTriangle className="size-5 text-rose-600" />
              </div>
              <div>
                <h3 className="text-base font-bold font-sans text-zinc-900">
                  Hapus Rekaman Lot Ini?
                </h3>
                <p className="text-xs font-mono font-semibold text-rose-700">
                  {lotId}
                </p>
              </div>
            </div>

            <p className="text-xs font-sans text-gray-600 leading-relaxed">
              Tindakan ini akan menghapus data audit inspeksi mutu, rekaman cacat mutu visual, dan mengosongkan alokasi slot penyimpanan terkait secara permanen.
            </p>

            {errorMsg && (
              <div className="p-2.5 bg-rose-50 border border-rose-200 rounded text-xs text-rose-700">
                {errorMsg}
              </div>
            )}

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                disabled={isDeleting}
                className="px-4 py-2 text-xs font-semibold font-sans text-gray-700 bg-slate-100 hover:bg-slate-200 rounded-sm transition-colors cursor-pointer disabled:opacity-50"
              >
                Batal
              </button>
              <button
                type="button"
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex items-center gap-1.5 px-4 py-2 text-xs font-bold font-sans text-white bg-rose-600 hover:bg-rose-700 rounded-sm transition-colors cursor-pointer shadow-xs disabled:opacity-50"
              >
                {isDeleting ? (
                  <>
                    <Loader2 className="size-3.5 animate-spin" />
                    <span>Menghapus...</span>
                  </>
                ) : (
                  <>
                    <Trash2 className="size-3.5" />
                    <span>Ya, Hapus Sekarang</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};


