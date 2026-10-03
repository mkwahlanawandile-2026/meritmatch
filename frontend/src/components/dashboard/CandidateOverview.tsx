import type { Candidate } from '../../types/meritmatch'
import StatusBadge from '../common/StatusBadge'

type CandidateOverviewProps = {
  candidate: Candidate
}

type ScoreRowProps = {
  label: string
  score: number
}

function ScoreRow({ label, score }: ScoreRowProps) {
  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between">
        <span className="text-[11px] font-medium text-slate-400">
          {label}
        </span>

        <span className="text-[11px] font-semibold text-white">
          {score}%
        </span>
      </div>

      <div className="h-1.5 overflow-hidden rounded-full bg-[#0B1220]">
        <div
          className="h-full rounded-full bg-[#4F7CFF] transition-all duration-300"
          style={{ width: `${Math.min(score, 100)}%` }}
        />
      </div>
    </div>
  )
}

export default function CandidateOverview({
  candidate,
}: CandidateOverviewProps) {
  return (
    <section className="rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
      <div className="flex items-start justify-between border-b border-white/10 px-5 py-5">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#243A68] text-sm font-semibold text-[#7EA2FF]">
            {candidate.name.slice(-1)}
          </div>

          <div>
            <h2 className="text-[16px] font-semibold text-white">
              {candidate.name}
            </h2>

            <p className="mt-1 text-[11px] text-slate-500">
              {candidate.role} · {candidate.experienceMonths} months experience
            </p>
          </div>
        </div>

        <StatusBadge status={candidate.status} />
      </div>

      <div className="grid grid-cols-1 gap-6 p-5 lg:grid-cols-[180px_1fr]">
        <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
          <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
            Overall Match
          </div>

          <div className="mt-3 text-[32px] font-semibold tracking-tight text-white">
            {candidate.overallScore.toFixed(1)}%
          </div>

          <div className="mt-1 text-[11px] text-slate-500">
            Candidate fit score
          </div>
        </div>

        <div className="space-y-4">
          <ScoreRow label="Skills" score={candidate.skillsScore} />
          <ScoreRow label="Experience" score={candidate.experienceScore} />
          <ScoreRow label="Education" score={candidate.educationScore} />
          <ScoreRow label="Semantic Match" score={candidate.semanticScore} />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 border-t border-white/10 px-5 py-5 md:grid-cols-2">
        <div>
          <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
            Strengths
          </div>

          <div className="space-y-2">
            {candidate.strengths.map((strength) => (
              <div
                key={strength}
                className="flex items-start gap-2 text-[12px] text-slate-400"
              >
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
                <span>{strength}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
            Requirement Gaps
          </div>

          <div className="space-y-2">
            {candidate.gaps.map((gap) => (
              <div
                key={gap}
                className="flex items-start gap-2 text-[12px] text-slate-400"
              >
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-400" />
                <span>{gap}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
