import {
  BarChart3,
  CheckCircle2,
  CircleAlert,
  Target,
  TrendingUp,
  Users,
} from 'lucide-react'
import { candidates } from '../data/demoData'

const statusCounts = {
  qualified: candidates.filter((candidate) => candidate.status === 'Qualified')
    .length,
  review: candidates.filter((candidate) => candidate.status === 'Review').length,
  notQualified: candidates.filter(
    (candidate) => candidate.status === 'Not Qualified',
  ).length,
}

const averageMatch =
  candidates.reduce((total, candidate) => total + candidate.overallScore, 0) /
  candidates.length

const averageSkills =
  candidates.reduce((total, candidate) => total + candidate.skillsScore, 0) /
  candidates.length

const averageExperience =
  candidates.reduce(
    (total, candidate) => total + candidate.experienceScore,
    0,
  ) / candidates.length

const averageEducation =
  candidates.reduce(
    (total, candidate) => total + candidate.educationScore,
    0,
  ) / candidates.length

const averageSemantic =
  candidates.reduce(
    (total, candidate) => total + candidate.semanticScore,
    0,
  ) / candidates.length

function ScoreBar({
  label,
  score,
  weight,
}: {
  label: string
  score: number
  weight: string
}) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <div>
          <span className="text-[12px] font-medium text-slate-300">
            {label}
          </span>

          <span className="ml-2 text-[10px] text-slate-600">
            {weight}
          </span>
        </div>

        <span className="text-[12px] font-semibold text-white">
          {score.toFixed(1)}%
        </span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-[#0B1220]">
        <div
          className="h-full rounded-full bg-[#4F7CFF]"
          style={{ width: `${Math.min(score, 100)}%` }}
        />
      </div>
    </div>
  )
}

export default function Analytics() {
  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1440px]">

        {/* Header */}
        <div className="mb-8">
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
            Recruitment Analytics
          </div>

          <h1 className="text-[28px] font-semibold tracking-tight text-white">
            Analytics
          </h1>

          <p className="mt-2 text-[14px] text-slate-400">
            Understand candidate matching performance across the recruitment workspace.
          </p>
        </div>

        {/* KPI Strip */}
        <section className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] text-slate-400">
              <Users size={16} className="text-[#7EA2FF]" />
              Candidates Evaluated
            </div>

            <div className="mt-3 text-[28px] font-semibold text-white">
              {candidates.length}
            </div>

            <div className="mt-1 text-[11px] text-slate-600">
              Current workspace
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] text-slate-400">
              <Target size={16} className="text-[#7EA2FF]" />
              Average Match
            </div>

            <div className="mt-3 text-[28px] font-semibold text-white">
              {averageMatch.toFixed(1)}%
            </div>

            <div className="mt-1 flex items-center gap-1 text-[11px] text-emerald-400">
              <TrendingUp size={12} />
              Matching performance
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] text-slate-400">
              <CheckCircle2 size={16} className="text-emerald-400" />
              Qualified
            </div>

            <div className="mt-3 text-[28px] font-semibold text-white">
              {statusCounts.qualified}
            </div>

            <div className="mt-1 text-[11px] text-slate-600">
              Meeting configured requirements
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] text-slate-400">
              <CircleAlert size={16} className="text-amber-400" />
              Requires Review
            </div>

            <div className="mt-3 text-[28px] font-semibold text-white">
              {statusCounts.review}
            </div>

            <div className="mt-1 text-[11px] text-slate-600">
              Needs recruiter attention
            </div>
          </div>

        </section>

        {/* Analytics Grid */}
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">

          {/* Match Components */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-6 flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <BarChart3 size={17} className="text-[#7EA2FF]" />

                  <h2 className="text-[15px] font-semibold text-white">
                    Match Components
                  </h2>
                </div>

                <p className="mt-1 text-[11px] text-slate-500">
                  Average performance by matching dimension
                </p>
              </div>
            </div>

            <div className="space-y-6">
              <ScoreBar
                label="Skills"
                score={averageSkills}
                weight="40% weight"
              />

              <ScoreBar
                label="Experience"
                score={averageExperience}
                weight="25% weight"
              />

              <ScoreBar
                label="Education"
                score={averageEducation}
                weight="15% weight"
              />

              <ScoreBar
                label="Semantic Match"
                score={averageSemantic}
                weight="20% weight"
              />
            </div>

          </section>

          {/* Qualification Distribution */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-6">
              <div className="flex items-center gap-2">
                <Target size={17} className="text-[#7EA2FF]" />

                <h2 className="text-[15px] font-semibold text-white">
                  Qualification Distribution
                </h2>
              </div>

              <p className="mt-1 text-[11px] text-slate-500">
                Current candidate decision outcomes
              </p>
            </div>

            <div className="space-y-5">

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-[12px] text-slate-300">
                    Qualified
                  </span>

                  <span className="text-[12px] font-semibold text-emerald-300">
                    {statusCounts.qualified}
                  </span>
                </div>

                <div className="h-2 rounded-full bg-[#0B1220]">
                  <div
                    className="h-full rounded-full bg-emerald-400"
                    style={{
                      width: `${
                        (statusCounts.qualified / candidates.length) * 100
                      }%`,
                    }}
                  />
                </div>
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-[12px] text-slate-300">
                    Review
                  </span>

                  <span className="text-[12px] font-semibold text-amber-300">
                    {statusCounts.review}
                  </span>
                </div>

                <div className="h-2 rounded-full bg-[#0B1220]">
                  <div
                    className="h-full rounded-full bg-amber-400"
                    style={{
                      width: `${
                        (statusCounts.review / candidates.length) * 100
                      }%`,
                    }}
                  />
                </div>
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-[12px] text-slate-300">
                    Not Qualified
                  </span>

                  <span className="text-[12px] font-semibold text-red-300">
                    {statusCounts.notQualified}
                  </span>
                </div>

                <div className="h-2 rounded-full bg-[#0B1220]">
                  <div
                    className="h-full rounded-full bg-red-400"
                    style={{
                      width: `${
                        (statusCounts.notQualified / candidates.length) * 100
                      }%`,
                    }}
                  />
                </div>
              </div>

            </div>

            <div className="mt-7 rounded-lg border border-white/10 bg-[#111827] p-4">
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                Decision Framework
              </div>

              <p className="mt-2 text-[11px] leading-5 text-slate-500">
                Qualification combines the configured overall score,
                mandatory requirements, and semantic matching rules.
              </p>
            </div>

          </section>

          {/* Candidate Performance */}
          <section className="overflow-hidden rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)] xl:col-span-2">

            <div className="border-b border-white/10 px-5 py-4">
              <h2 className="text-[15px] font-semibold text-white">
                Candidate Performance
              </h2>

              <p className="mt-1 text-[11px] text-slate-500">
                Candidate-level matching results
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full min-w-[800px] border-collapse">

                <thead>
                  <tr className="border-b border-white/10 bg-[#111827] text-left">
                    <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Candidate
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Overall
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Skills
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Experience
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Education
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Semantic
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Decision
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {candidates.map((candidate) => (
                    <tr
                      key={candidate.id}
                      className="border-b border-white/5 last:border-b-0 hover:bg-white/[0.03]"
                    >
                      <td className="px-5 py-4">
                        <div className="text-[13px] font-medium text-white">
                          {candidate.name}
                        </div>

                        <div className="mt-0.5 text-[11px] text-slate-600">
                          {candidate.role}
                        </div>
                      </td>

                      <td className="px-4 py-4 text-[13px] font-semibold text-[#7EA2FF]">
                        {candidate.overallScore.toFixed(1)}%
                      </td>

                      <td className="px-4 py-4 text-[12px] text-slate-400">
                        {candidate.skillsScore}%
                      </td>

                      <td className="px-4 py-4 text-[12px] text-slate-400">
                        {candidate.experienceScore}%
                      </td>

                      <td className="px-4 py-4 text-[12px] text-slate-400">
                        {candidate.educationScore}%
                      </td>

                      <td className="px-4 py-4 text-[12px] text-slate-400">
                        {candidate.semanticScore}%
                      </td>

                      <td className="px-4 py-4">
                        <span
                          className={`inline-flex rounded-full border px-2.5 py-1 text-[11px] font-medium ${
                            candidate.status === 'Qualified'
                              ? 'border-emerald-400/20 bg-emerald-400/10 text-emerald-300'
                              : candidate.status === 'Review'
                                ? 'border-amber-400/20 bg-amber-400/10 text-amber-300'
                                : 'border-red-400/20 bg-red-400/10 text-red-300'
                          }`}
                        >
                          {candidate.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>

              </table>
            </div>

          </section>

        </div>
      </div>
    </main>
  )
}
