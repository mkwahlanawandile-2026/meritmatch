import { Search, SlidersHorizontal, UserRound } from 'lucide-react'
import { useMemo, useState } from 'react'
import StatusBadge from '../components/common/StatusBadge'
import { candidates } from '../data/demoData'
import type { Candidate } from '../types/meritmatch'

export default function Candidates() {
  const [search, setSearch] = useState('')
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate>(
    candidates[0],
  )

  const filteredCandidates = useMemo(() => {
    const query = search.toLowerCase().trim()

    if (!query) {
      return candidates
    }

    return candidates.filter(
      (candidate) =>
        candidate.name.toLowerCase().includes(query) ||
        candidate.role.toLowerCase().includes(query) ||
        candidate.strengths.some((strength) =>
          strength.toLowerCase().includes(query),
        ),
    )
  }, [search])

  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1440px]">

        {/* Header */}
        <div className="mb-7">
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
            Candidate Intelligence
          </div>

          <h1 className="text-[28px] font-semibold tracking-tight text-white">
            Candidates
          </h1>

          <p className="mt-2 text-[14px] text-slate-400">
            Review candidate profiles and evaluate their fit against employer-defined requirements.
          </p>
        </div>

        {/* Search / Controls */}
        <section className="mb-6 flex flex-col gap-3 rounded-xl border border-white/10 bg-[#151F33] p-4 shadow-[0_8px_24px_rgba(0,0,0,0.18)] md:flex-row md:items-center md:justify-between">
          <div className="flex h-10 w-full items-center gap-2.5 rounded-lg border border-white/10 bg-[#0B1220] px-3 md:max-w-[420px]">
            <Search size={16} className="shrink-0 text-slate-500" />

            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search candidates, roles or skills..."
              className="w-full bg-transparent text-[12px] text-white outline-none placeholder:text-slate-600"
            />
          </div>

          <button
            type="button"
            className="flex h-10 items-center justify-center gap-2 rounded-lg border border-white/10 bg-[#111827] px-4 text-[12px] font-medium text-slate-300 transition hover:bg-white/5 hover:text-white"
          >
            <SlidersHorizontal size={15} />
            Filters
          </button>
        </section>

        {/* Main Workspace */}
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_390px]">

          {/* Candidate List */}
          <section className="overflow-hidden rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Candidate Pool
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  {filteredCandidates.length} candidate
                  {filteredCandidates.length === 1 ? '' : 's'} available
                </p>
              </div>

              <span className="rounded-full border border-white/10 bg-white/5 px-2.5 py-1 text-[10px] font-medium text-slate-400">
                {filteredCandidates.length} results
              </span>
            </div>

            <div className="divide-y divide-white/5">
              {filteredCandidates.map((candidate) => {
                const selected = candidate.id === selectedCandidate.id

                return (
                  <button
                    key={candidate.id}
                    type="button"
                    onClick={() => setSelectedCandidate(candidate)}
                    className={`flex w-full items-center justify-between gap-5 px-5 py-4 text-left transition ${
                      selected
                        ? 'bg-[#1D2B47]'
                        : 'hover:bg-white/[0.03]'
                    }`}
                  >
                    <div className="flex min-w-0 items-center gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                        <UserRound size={17} />
                      </div>

                      <div className="min-w-0">
                        <div className="text-[13px] font-semibold text-white">
                          {candidate.name}
                        </div>

                        <div className="mt-0.5 truncate text-[11px] text-slate-500">
                          {candidate.role}
                        </div>
                      </div>
                    </div>

                    <div className="flex shrink-0 items-center gap-4">
                      <div className="hidden text-right sm:block">
                        <div className="text-[10px] uppercase tracking-[0.1em] text-slate-600">
                          Match
                        </div>

                        <div className="mt-1 text-[13px] font-semibold text-[#7EA2FF]">
                          {candidate.overallScore.toFixed(1)}%
                        </div>
                      </div>

                      <StatusBadge status={candidate.status} />
                    </div>
                  </button>
                )
              })}

              {filteredCandidates.length === 0 && (
                <div className="px-5 py-12 text-center">
                  <div className="text-[13px] font-medium text-slate-300">
                    No candidates found
                  </div>

                  <div className="mt-1 text-[11px] text-slate-600">
                    Try a different name, role or skill.
                  </div>
                </div>
              )}
            </div>
          </section>

          {/* Candidate Detail */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="border-b border-white/10 p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#243A68] text-[#7EA2FF]">
                    <UserRound size={20} />
                  </div>

                  <div>
                    <h2 className="text-[16px] font-semibold text-white">
                      {selectedCandidate.name}
                    </h2>

                    <p className="mt-1 text-[11px] text-slate-500">
                      {selectedCandidate.role}
                    </p>
                  </div>
                </div>

                <StatusBadge status={selectedCandidate.status} />
              </div>
            </div>

            {/* Overall Score */}
            <div className="border-b border-white/10 p-5">
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Overall Match
              </div>

              <div className="mt-2 flex items-end justify-between">
                <span className="text-[34px] font-semibold tracking-tight text-white">
                  {selectedCandidate.overallScore.toFixed(1)}%
                </span>

                <span className="mb-1 text-[11px] text-slate-500">
                  {selectedCandidate.experienceMonths} months experience
                </span>
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="border-b border-white/10 p-5">
              <div className="mb-4 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Match Breakdown
              </div>

              <div className="space-y-4">
                {[
                  ['Skills', selectedCandidate.skillsScore],
                  ['Experience', selectedCandidate.experienceScore],
                  ['Education', selectedCandidate.educationScore],
                  ['Semantic Match', selectedCandidate.semanticScore],
                ].map(([label, score]) => (
                  <div key={label}>
                    <div className="mb-1.5 flex justify-between">
                      <span className="text-[11px] text-slate-400">
                        {label}
                      </span>

                      <span className="text-[11px] font-semibold text-white">
                        {score}%
                      </span>
                    </div>

                    <div className="h-1.5 rounded-full bg-[#0B1220]">
                      <div
                        className="h-full rounded-full bg-[#4F7CFF]"
                        style={{ width: `${score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Strengths */}
            <div className="border-b border-white/10 p-5">
              <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Strengths
              </div>

              <div className="space-y-2">
                {selectedCandidate.strengths.map((strength) => (
                  <div
                    key={strength}
                    className="flex items-start gap-2 text-[12px] text-slate-400"
                  >
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
                    {strength}
                  </div>
                ))}
              </div>
            </div>

            {/* Gaps */}
            <div className="p-5">
              <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Requirement Gaps
              </div>

              <div className="space-y-2">
                {selectedCandidate.gaps.map((gap) => (
                  <div
                    key={gap}
                    className="flex items-start gap-2 text-[12px] text-slate-400"
                  >
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-400" />
                    {gap}
                  </div>
                ))}
              </div>
            </div>

          </section>
        </div>
      </div>
    </main>
  )
}
