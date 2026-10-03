import { Bell, Search } from 'lucide-react'

export default function Topbar() {
  return (
    <header className="flex h-[72px] items-center justify-between border-b border-white/10 bg-[#111827] px-7">
      <div>
        <div className="text-[13px] font-medium text-slate-200">
          Recruitment workspace
        </div>

        <div className="mt-0.5 text-[11px] text-slate-500">
          MeritMatch candidate intelligence
        </div>
      </div>

      <div className="flex items-center gap-5">
        <div className="flex h-9 w-[230px] items-center gap-2.5 rounded-lg border border-white/10 bg-[#0B1220] px-3">
          <Search size={16} className="text-slate-500" />

          <input
            type="text"
            placeholder="Search candidates..."
            className="w-full bg-transparent text-[12px] text-white outline-none placeholder:text-slate-600"
          />
        </div>

        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-white/5 hover:text-white"
        >
          <Bell size={18} strokeWidth={1.8} />

          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#4F7CFF]" />
        </button>

        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#356AE6] text-[12px] font-semibold text-white">
          M
        </div>
      </div>
    </header>
  )
}
