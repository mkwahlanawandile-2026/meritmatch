import {
  CheckCircle2,
  ChevronRight,
  GitCompare,
  ShieldCheck,
  SlidersHorizontal,
} from 'lucide-react'
import { useState } from 'react'
import StatusBadge from '../components/common/StatusBadge'
import { activeJob, candidates } from '../data/demoData'
import type { Candidate } from '../types/meritmatch'

export default function Matches() {
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate>(
    candidates[0],
  )

  const sortedCandidates = [...candidates].sort(
    (a, b) => b.overallScore - a.overallScore,
  )

  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1440px]">

        {/* Header */}
        <div className="mb-7 flex items-start justify-between gap-6">
          <div>
            <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
              Matching Intelligence
            </div>

            <h1 className="text-[28px] font-semibold tracking-tight text-white">
              Matches
            </h1>

            <p className="mt-2 text-[14px] text-slate-400">
              Rank candidates against employer-defined job requirements.
            </p>
          </div>

          <button
            type="button"
            className="flex items-center gap-2 rounded-lg border border-white/10 bg-[#151F33] px-4 py-2.5 text-[12px] font-medium text-slate-300 transition hover:bg-white/5 hover:text-white"
          >
            <SlidersHorizontal size={15} />
            Matching Rules
          </button>
        </div>

        {/* Active Job */}
        <section className="mb-6 rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
          <div className="flex flex-col gap-5 p-5 lg:flex-row lg:items-center lg:justify-between">

            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#243A68] text-[#7EA2FF]">
                <GitCompare size={20} />
              </div>

              <div>
                <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                  Active Position
                </div>

                <h2 className="mt-1 text-[17px] font-semibold text-white">
                  {activeJob.title}
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  {activeJob.department} · {activeJob.location} ·{' '}
                  {activeJob.employmentType}
                </p>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {activeJob.requiredSkills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-blue-400/20 bg-blue-400/10 px-2.5 py-1 text-[10px] font-medium text-blue-300"
                >
                  Required: {skill}
                </span>
              ))}

              {activeJob.preferredSkills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-white/10 bg-white/5 px-2.5 py-1 text-[10px] font-medium text-slate-400"
                >
                  Preferred: {skill}
                </span>
              ))}
            </div>

          </div>
        </section>

        {/* Main Content */}
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_390px]">

          {/* Ranking */}
          <section className="overflow-hidden rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Candidate Ranking
                </h2>

                <p className="mt-1 text-[11px] text-slate-500">
                  Ordered by overall matching score
                </p>
              </div>

              <span className="text-[11px] text-slate-500">
                {sortedCandidates.length} evaluated
              </span>
            </div>

            <div className="divide-y divide-white/5">

              {sortedCandidates.map((candidate, index) => {
                const selected = candidate.id === selectedCandidate.id

                return (
                  <button
                    key={candidate.id}
                    type="button"
                    onClick={() => setSelectedCandidate(candidate)}
                    className={`flex w-full items-center gap-4 px-5 py-4 text-left transition ${
                      selected
                        ? 'bg-[#1D2B47]'
                        : 'hover:bg-white/[0.03]'
                    }`}
                  >

                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#111827] text-[11px] font-semibold text-slate-400">
                      #{index + 1}
                    </div>

                    <div className="flex min-w-0 flex-1 items-center gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#243A68] text-[11px] font-semibold text-[#7EA2FF]">
                        {candidate.name.slice(-1)}
                      </div>

                      <div className="min-w-0">
                        <div className="text-[13px] font-semibold text-white">
                          {candidate.name}
                        </div>

                        <div className="mt-0.5 text-[11px] text-slate-500">
                          {candidate.role}
                        </div>
                      </div>
                    </div>

                    <div className="hidden text-right sm:block">
                      <div className="text-[10px] uppercase tracking-[0.1em] text-slate-600">
                        Skills
                      </div>

                      <div className="mt-1 text-[12px] font-medium text-slate-300">
                        {candidate.skillsScore}%
                      </div>
                    </div>

                    <div className="hidden text-right md:block">
                      <div className="text-[10px] uppercase tracking-[0.1em] text-slate-600">
                        Experience
                      </div>

                      <div className="mt-1 text-[12px] font-medium text-slate-300">
                        {candidate.experienceScore}%
                      </div>
                    </div>

                    <div className="w-[72px] text-right">
                      <div className="text-[16px] font-semibold text-[#7EA2FF]">
                        {candidate.overallScore.toFixed(1)}%
                      </div>

                      <div className="mt-1">
                        <StatusBadge status={candidate.status} />
                      </div>
                    </div>

                    <ChevronRight
                      size={16}
                      className="shrink-0 text-slate-600"
                    />

                  </button>
                )
              })}

            </div>
          </section>

          {/* Explanation Panel */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="border-b border-white/10 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Match Explanation
                  </div>

                  <h2 className="mt-1 text-[17px] font-semibold text-white">
                    {selectedCandidate.name}
                  </h2>
                </div>

                <div className="text-right">
                  <div className="text-[26px] font-semibold text-[#7EA2FF]">
                    {selectedCandidate.overallScore.toFixed(1)}%
                  </div>

                  <div className="text-[10px] text-slate-500">
                    overall score
                  </div>
                </div>
              </div>
            </div>

            {/* Qualification */}
            <div className="border-b border-white/10 p-5">
              <div className="flex items-center gap-3 rounded-lg border border-emerald-400/20 bg-emerald-400/10 p-3">
                <CheckCircle2
                  size={18}
                  className="shrink-0 text-emerald-400"
                />

                <div>
                  <div className="text-[12px] font-semibold text-emerald-300">
                    {selectedCandidate.status}
                  </div>

                  <div className="mt-0.5 text-[10px] text-emerald-300/60">
                    Matching decision based on configured requirements
                  </div>
                </div>
              </div>
            </div>

            {/* Score Components */}
            <div className="border-b border-white/10 p-5">
              <div className="mb-4 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Score Components
              </div>

              <div className="space-y-3">

                {[
                  ['Skills', selectedCandidate.skillsScore, '40% weight'],
                  [
                    'Experience',
                    selectedCandidate.experienceScore,
                    '25% weight',
                  ],
                  [
                    'Education',
                    selectedCandidate.educationScore,
                    '15% weight',
                  ],
                  [
                    'Semantic',
                    selectedCandidate.semanticScore,
                    '20% weight',
                  ],
                ].map(([label, score, weight]) => (
                  <div
                    key={label}
                    className="flex items-center justify-between"
                  >
                    <div>
                      <div className="text-[12px] text-slate-300">
                        {label}
                      </div>

                      <div className="mt-0.5 text-[10px] text-slate-600">
                        {weight}
                      </div>
                    </div>

                    <span className="text-[12px] font-semibold text-white">
                      {score}%
                    </span>
                  </div>
                ))}

              </div>
            </div>

            {/* Requirements */}
            <div className="border-b border-white/10 p-5">
              <div className="mb-4 flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                <ShieldCheck size={14} />
                Requirement Analysis
              </div>

              <div className="space-y-3">

                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-slate-400">
                    Required skills
                  </span>

                  <span className="text-[11px] font-medium text-emerald-300">
                    Satisfied
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-slate-400">
                    Minimum experience
                  </span>

                  <span className="text-[11px] font-medium text-emerald-300">
                    {selectedCandidate.experienceMonths >=
                    activeJob.minimumExperienceMonths
                      ? 'Satisfied'
                      : 'Below requirement'}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-slate-400">
                    Semantic threshold
                  </span>

                  <span className="text-[11px] font-medium text-emerald-300">
                    Satisfied
                  </span>
                </div>

              </div>
            </div>

            {/* Strengths */}
            <div className="p-5">
              <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Key Evidence
              </div>

              <div className="space-y-2">
                {selectedCandidate.strengths.map((strength) => (
                  <div
                    key={strength}
                    className="flex items-start gap-2 text-[11px] text-slate-400"
                  >
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
                    {strength}
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
