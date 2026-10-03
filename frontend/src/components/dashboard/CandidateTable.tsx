import type { Candidate } from '../../types/meritmatch'
import StatusBadge from '../common/StatusBadge'

type CandidateTableProps = {
  candidates: Candidate[]
  selectedCandidateId: string
  onSelectCandidate: (candidate: Candidate) => void
}

export default function CandidateTable({
  candidates,
  selectedCandidateId,
  onSelectCandidate,
}: CandidateTableProps) {
  return (
    <section className="overflow-hidden rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
      <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
        <div>
          <h2 className="text-[15px] font-semibold text-white">
            Top Candidates
          </h2>

          <p className="mt-1 text-[11px] text-slate-500">
            Ranked against the active employer-defined requirements
          </p>
        </div>

        <span className="text-[11px] font-medium text-slate-500">
          {candidates.length} evaluated
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] border-collapse">
          <thead>
            <tr className="border-b border-white/10 bg-[#111827] text-left">
              <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Candidate
              </th>

              <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Match
              </th>

              <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Skills
              </th>

              <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Experience
              </th>

              <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Status
              </th>
            </tr>
          </thead>

          <tbody>
            {candidates.map((candidate) => {
              const selected = candidate.id === selectedCandidateId

              return (
                <tr
                  key={candidate.id}
                  onClick={() => onSelectCandidate(candidate)}
                  className={`cursor-pointer border-b border-white/5 transition last:border-b-0 ${
                    selected
                      ? 'bg-[#1D2B47]'
                      : 'hover:bg-white/[0.03]'
                  }`}
                >
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[11px] font-semibold text-[#7EA2FF]">
                        {candidate.name.slice(-1)}
                      </div>

                      <div>
                        <div className="text-[13px] font-medium text-white">
                          {candidate.name}
                        </div>

                        <div className="mt-0.5 text-[11px] text-slate-500">
                          {candidate.role}
                        </div>
                      </div>
                    </div>
                  </td>

                  <td className="px-4 py-4">
                    <span className="text-[13px] font-semibold text-white">
                      {candidate.overallScore.toFixed(1)}%
                    </span>
                  </td>

                  <td className="px-4 py-4 text-[12px] font-medium text-slate-400">
                    {candidate.skillsScore}%
                  </td>

                  <td className="px-4 py-4 text-[12px] font-medium text-slate-400">
                    {candidate.experienceScore}%
                  </td>

                  <td className="px-4 py-4">
                    <StatusBadge status={candidate.status} />
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </section>
  )
}
