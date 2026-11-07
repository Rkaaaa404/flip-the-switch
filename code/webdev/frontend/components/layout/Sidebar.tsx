"use client";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  ScanLine,
  History,
  Boxes,
  Truck,
  Settings,
  LogOut,
} from "lucide-react";
import Link from "next/link";

export const Sidebar = () => {
  const pathname = usePathname();
  const isActive = (href: string) => {
    if (href === "/") return pathname === href;
    return pathname.startsWith(href);
  };

  const navItems = [
    { href: "/", label: "Dashboard", icon: LayoutDashboard },
    { href: "/inspection", label: "Inspection", icon: ScanLine },
    { href: "/history", label: "Lot History", icon: History },
    { href: "/storage", label: "Lot Storage", icon: Boxes },
    { href: "/dispatch", label: "Export Dispatch", icon: Truck },
    { href: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside className="h-screen sticky top-0 bg-slate-900 flex flex-col shadow-lg overflow-y-auto overflow-x-hidden w-64 shrink-0 border-r border-slate-800">
      <div className="h-16 px-4 border-b border-slate-800 flex items-center gap-3 bg-slate-950">
        <img className="w-8 h-8 object-contain" src="/logo.svg" alt="NusaQC Logo" />
        <div className="flex flex-col">
          <span className="text-white text-lg font-bold font-sans leading-tight">
            NusaQC
          </span>
          <span className="text-sky-400 text-[10px] font-bold font-sans uppercase tracking-wider">
            Fish Processing AI
          </span>
        </div>
      </div>

      <nav className="flex flex-col gap-1 mt-4 flex-1 px-2">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={`px-3 py-3 rounded-md inline-flex items-center gap-3 transition-colors ${
              isActive(href)
                ? "bg-slate-800 text-sky-400 font-semibold border-l-4 border-sky-500"
                : "text-slate-400 font-medium hover:bg-slate-800/50 hover:text-slate-200"
            }`}
          >
            <Icon className={`size-4 ${isActive(href) ? "text-sky-400" : "text-slate-400"}`} />
            <span className="text-sm font-sans">
              {label}
            </span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-white/10 flex justify-between items-center mt-auto">
        <div className="flex items-center gap-3">
          <div className="size-8 bg-sky-500 rounded-full flex justify-center items-center">
            <span className="text-white text-xs font-bold font-sans">
              QC
            </span>
          </div>
          <div className="flex flex-col">
            <span className="text-white text-xs font-medium font-sans">
              QC Supervisor
            </span>
            <span className="text-white/40 text-[10px] font-sans">
              Active Session
            </span>
          </div>
        </div>
        <LogOut className="size-4 text-slate-400 cursor-pointer hover:text-white transition-colors" />
      </div>
    </aside>
  );
};
