type MetricCardProps = {
  label: string
  value: string
  detail: string
  accent?: string
}

export default function MetricCard({
  label,
  value,
  detail,
  accent = '#4F7CFF',
}: MetricCardProps) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#151F33] px-5 py-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
      <div className="flex items-center justify-between">
        <span className="text-[12px] font-medium text-slate-400">
          {label}
        </span>

        <span
          className="h-2 w-2 rounded-full"
          style={{ backgroundColor: accent }}
        />
      </div>

      <div className="mt-4 text-[27px] font-semibold tracking-tight text-white">
        {value}
      </div>

      <div className="mt-1 text-[11px] text-slate-500">
        {detail}
      </div>
    </div>
  )
}
