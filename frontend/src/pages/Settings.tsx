import {
  BrainCircuit,
  CheckCircle2,
  FileText,
  LockKeyhole,
  Settings as SettingsIcon,
  ShieldCheck,
  SlidersHorizontal,
} from 'lucide-react'

function SettingRow({
  label,
  description,
  value,
}: {
  label: string
  description: string
  value: React.ReactNode
}) {
  return (
    <div className="flex items-center justify-between gap-6 border-b border-white/5 py-4 last:border-b-0">
      <div>
        <div className="text-[12px] font-medium text-slate-200">
          {label}
        </div>

        <div className="mt-1 max-w-[620px] text-[11px] leading-5 text-slate-600">
          {description}
        </div>
      </div>

      <div className="shrink-0">
        {value}
      </div>
    </div>
  )
}

function WeightBar({
  label,
  weight,
}: {
  label: string
  weight: number
}) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <span className="text-[11px] text-slate-400">
          {label}
        </span>

        <span className="text-[11px] font-semibold text-white">
          {weight}%
        </span>
      </div>

      <div className="h-1.5 overflow-hidden rounded-full bg-[#0B1220]">
        <div
          className="h-full rounded-full bg-[#4F7CFF]"
          style={{ width: `${weight}%` }}
        />
      </div>
    </div>
  )
}

export default function Settings() {
  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1200px]">

        {/* Header */}
        <div className="mb-8">
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
            System Configuration
          </div>

          <h1 className="text-[28px] font-semibold tracking-tight text-white">
            Settings
          </h1>

          <p className="mt-2 text-[14px] text-slate-400">
            Configure how MeritMatch processes candidates and evaluates employer-defined requirements.
          </p>
        </div>

        {/* System Status */}
        <section className="mb-6 rounded-xl border border-emerald-400/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
          <div className="flex items-center justify-between gap-5">

            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-400/10 text-emerald-400">
                <CheckCircle2 size={19} />
              </div>

              <div>
                <div className="text-[14px] font-semibold text-white">
                  Matching Engine Operational
                </div>

                <div className="mt-1 text-[11px] text-slate-500">
                  MeritMatch configuration is loaded and ready for candidate evaluation.
                </div>
              </div>
            </div>

            <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-[11px] font-medium text-emerald-300">
              Operational
            </span>

          </div>
        </section>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">

          {/* Matching Configuration */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-5 flex items-start gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                <SlidersHorizontal size={17} />
              </div>

              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Matching Configuration
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  Weights used to calculate the overall candidate match score.
                </p>
              </div>
            </div>

            <div className="space-y-5">
              <WeightBar label="Skills" weight={40} />
              <WeightBar label="Experience" weight={25} />
              <WeightBar label="Education" weight={15} />
              <WeightBar label="Semantic Match" weight={20} />
            </div>

            <div className="mt-6 rounded-lg border border-white/10 bg-[#111827] p-4">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                  Total Weight
                </span>

                <span className="text-[13px] font-semibold text-emerald-300">
                  100%
                </span>
              </div>
            </div>
          </section>

          {/* Qualification Rules */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-3 flex items-start gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                <ShieldCheck size={17} />
              </div>

              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Qualification Rules
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  Rules applied when determining candidate qualification.
                </p>
              </div>
            </div>

            <SettingRow
              label="Minimum Overall Score"
              description="Minimum overall match score required for qualification."
              value={
                <span className="rounded-md border border-[#4F7CFF]/20 bg-[#4F7CFF]/10 px-3 py-1.5 text-[12px] font-semibold text-[#A9BEFF]">
                  70%
                </span>
              }
            />

            <SettingRow
              label="Semantic Threshold"
              description="Minimum semantic similarity required by the matching engine."
              value={
                <span className="rounded-md border border-[#4F7CFF]/20 bg-[#4F7CFF]/10 px-3 py-1.5 text-[12px] font-semibold text-[#A9BEFF]">
                  75%
                </span>
              }
            />

            <SettingRow
              label="Mandatory Requirements"
              description="Employer-defined mandatory requirements must be satisfied."
              value={
                <span className="flex items-center gap-1.5 text-[11px] font-medium text-emerald-300">
                  <CheckCircle2 size={14} />
                  Enabled
                </span>
              }
            />

          </section>

          {/* AI Engine */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-3 flex items-start gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                <BrainCircuit size={17} />
              </div>

              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  AI Matching Engine
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  Semantic and intelligence-layer configuration.
                </p>
              </div>
            </div>

            <SettingRow
              label="Semantic Model"
              description="Embedding model used for semantic requirement matching."
              value={
                <span className="rounded-md border border-white/10 bg-[#111827] px-3 py-1.5 font-mono text-[10px] text-slate-300">
                  all-MiniLM-L6-v2
                </span>
              }
            />

            <SettingRow
              label="Matching Engine"
              description="Core Python intelligence layer responsible for candidate evaluation."
              value={
                <span className="text-[11px] font-medium text-emerald-300">
                  Ready
                </span>
              }
            />

            <SettingRow
              label="Explainability"
              description="Match results include strengths, gaps, scores, and decision reasons."
              value={
                <span className="flex items-center gap-1.5 text-[11px] font-medium text-emerald-300">
                  <CheckCircle2 size={14} />
                  Enabled
                </span>
              }
            />

          </section>

          {/* Privacy & Processing */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-3 flex items-start gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                <LockKeyhole size={17} />
              </div>

              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Privacy & Processing
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  Candidate-data processing configuration.
                </p>
              </div>
            </div>

            <SettingRow
              label="Anonymization"
              description="Candidate information is anonymized by default during matching workflows."
              value={
                <span className="flex items-center gap-1.5 text-[11px] font-medium text-emerald-300">
                  <CheckCircle2 size={14} />
                  Default
                </span>
              }
            />

            <SettingRow
              label="Supported Resume Formats"
              description="Accepted candidate document formats."
              value={
                <div className="flex items-center gap-1.5">
                  {['PDF', 'DOCX', 'TXT'].map((format) => (
                    <span
                      key={format}
                      className="rounded-md border border-white/10 bg-[#111827] px-2 py-1 text-[10px] font-medium text-slate-400"
                    >
                      {format}
                    </span>
                  ))}
                </div>
              }
            />

            <SettingRow
              label="Maximum File Size"
              description="Maximum supported resume upload size."
              value={
                <span className="text-[11px] font-medium text-white">
                  5 MB
                </span>
              }
            />

          </section>

          {/* Platform Information */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)] xl:col-span-2">

            <div className="mb-5 flex items-start gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                <SettingsIcon size={17} />
              </div>

              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Platform Information
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  MeritMatch application and architecture information.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-3 md:grid-cols-3">

              <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
                <div className="flex items-center gap-2 text-[11px] text-slate-500">
                  <FileText size={14} />
                  Frontend
                </div>

                <div className="mt-3 text-[13px] font-medium text-white">
                  React + TypeScript
                </div>

                <div className="mt-1 text-[10px] text-slate-600">
                  Tailwind CSS interface
                </div>
              </div>

              <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
                <div className="flex items-center gap-2 text-[11px] text-slate-500">
                  <BrainCircuit size={14} />
                  Intelligence Layer
                </div>

                <div className="mt-3 text-[13px] font-medium text-white">
                  Python
                </div>

                <div className="mt-1 text-[10px] text-slate-600">
                  NLP + semantic matching
                </div>
              </div>

              <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
                <div className="flex items-center gap-2 text-[11px] text-slate-500">
                  <ShieldCheck size={14} />
                  Decision Support
                </div>

                <div className="mt-3 text-[13px] font-medium text-white">
                  Employer-defined
                </div>

                <div className="mt-1 text-[10px] text-slate-600">
                  Human decision remains final
                </div>
              </div>

            </div>

            <div className="mt-5 border-t border-white/10 pt-4">
              <div className="flex items-center justify-between gap-4">
                <span className="text-[10px] text-slate-600">
                  MeritMatch version 0.1 · Development
                </span>

                <span className="flex items-center gap-1.5 text-[10px] text-emerald-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                  System ready
                </span>
              </div>
            </div>

          </section>

        </div>
      </div>
    </main>
  )
}
