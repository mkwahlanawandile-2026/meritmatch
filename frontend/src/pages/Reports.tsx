import {
  BarChart3,
  BriefcaseBusiness,
  CheckCircle2,
  Download,
  FileText,
  ShieldCheck,
  Target,
  Users,
} from 'lucide-react'
import { activeJob, candidates } from '../data/demoData'

const qualified = candidates.filter(
  (candidate) => candidate.status === 'Qualified',
).length

const review = candidates.filter(
  (candidate) => candidate.status === 'Review',
).length

const averageMatch =
  candidates.reduce((total, candidate) => total + candidate.overallScore, 0) /
  candidates.length

const sortedCandidates = [...candidates].sort(
  (a, b) => b.overallScore - a.overallScore,
)

const averageScores = {
  skills:
    candidates.reduce((total, candidate) => total + candidate.skillsScore, 0) /
    candidates.length,

  experience:
    candidates.reduce(
      (total, candidate) => total + candidate.experienceScore,
      0,
    ) / candidates.length,

  education:
    candidates.reduce(
      (total, candidate) => total + candidate.educationScore,
      0,
    ) / candidates.length,

  semantic:
    candidates.reduce(
      (total, candidate) => total + candidate.semanticScore,
      0,
    ) / candidates.length,
}

function SectionTitle({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <div className="mb-5 flex items-start gap-3">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
        {icon}
      </div>

      <div>
        <h2 className="text-[15px] font-semibold text-white">
          {title}
        </h2>

        <p className="mt-1 text-[11px] text-slate-500">
          {description}
        </p>
      </div>
    </div>
  )
}

function ScoreBar({
  label,
  score,
}: {
  label: string
  score: number
}) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <span className="text-[11px] text-slate-400">
          {label}
        </span>

        <span className="text-[11px] font-semibold text-white">
          {score.toFixed(1)}%
        </span>
      </div>

      <div className="h-1.5 overflow-hidden rounded-full bg-[#0B1220]">
        <div
          className="h-full rounded-full bg-[#4F7CFF]"
          style={{ width: `${Math.min(score, 100)}%` }}
        />
      </div>
    </div>
  )
}

export default function Reports() {
  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1440px]">

        {/* Header */}
        <div className="mb-8 flex items-start justify-between gap-6">
          <div>
            <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
              Recruitment Reporting
            </div>

            <h1 className="text-[28px] font-semibold tracking-tight text-white">
              Recruitment Report
            </h1>

            <p className="mt-2 text-[14px] text-slate-400">
              Structured summary of candidate matching results and employer-defined requirements.
            </p>
          </div>

          <button
            type="button"
            className="flex items-center gap-2 rounded-lg bg-[#356AE6] px-4 py-2.5 text-[12px] font-semibold text-white shadow-[0_6px_18px_rgba(53,106,230,0.25)] transition hover:bg-[#4377F0]"
          >
            <Download size={16} strokeWidth={2} />
            Export Report
          </button>
        </div>

        {/* Report Identity */}
        <section className="mb-6 rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-[1.5fr_1fr_1fr_1fr]">

            <div>
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                Active Position
              </div>

              <div className="mt-2 flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                  <BriefcaseBusiness size={17} />
                </div>

                <div>
                  <div className="text-[15px] font-semibold text-white">
                    {activeJob.title}
                  </div>

                  <div className="mt-0.5 text-[11px] text-slate-500">
                    {activeJob.department}
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                Work Arrangement
              </div>

              <div className="mt-3 text-[13px] font-medium text-white">
                {activeJob.workArrangement}
              </div>

              <div className="mt-1 text-[11px] text-slate-500">
                {activeJob.employmentType}
              </div>
            </div>

            <div>
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                Experience
              </div>

              <div className="mt-3 text-[13px] font-medium text-white">
                {activeJob.minimumExperienceMonths} months minimum
              </div>

              <div className="mt-1 text-[11px] text-slate-500">
                Employer-defined requirement
              </div>
            </div>

            <div>
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                Report Status
              </div>

              <div className="mt-3 flex items-center gap-2 text-[13px] font-medium text-emerald-300">
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                Matching complete
              </div>

              <div className="mt-1 text-[11px] text-slate-500">
                {candidates.length} candidates evaluated
              </div>
            </div>

          </div>
        </section>

        {/* Executive Summary */}
        <section className="mb-6 rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

          <SectionTitle
            icon={<FileText size={17} />}
            title="Executive Summary"
            description="High-level view of the current recruitment matching cycle."
          />

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">

            <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
              <div className="flex items-center gap-2 text-[11px] text-slate-500">
                <Users size={14} />
                Candidates Evaluated
              </div>

              <div className="mt-3 text-[24px] font-semibold text-white">
                {candidates.length}
              </div>
            </div>

            <div className="rounded-lg border border-emerald-400/10 bg-emerald-400/[0.04] p-4">
              <div className="flex items-center gap-2 text-[11px] text-slate-500">
                <CheckCircle2 size={14} className="text-emerald-400" />
                Qualified
              </div>

              <div className="mt-3 text-[24px] font-semibold text-emerald-300">
                {qualified}
              </div>
            </div>

            <div className="rounded-lg border border-amber-400/10 bg-amber-400/[0.04] p-4">
              <div className="flex items-center gap-2 text-[11px] text-slate-500">
                <Target size={14} className="text-amber-400" />
                Review
              </div>

              <div className="mt-3 text-[24px] font-semibold text-amber-300">
                {review}
              </div>
            </div>

            <div className="rounded-lg border border-[#4F7CFF]/10 bg-[#4F7CFF]/[0.04] p-4">
              <div className="flex items-center gap-2 text-[11px] text-slate-500">
                <BarChart3 size={14} className="text-[#7EA2FF]" />
                Average Match
              </div>

              <div className="mt-3 text-[24px] font-semibold text-[#7EA2FF]">
                {averageMatch.toFixed(1)}%
              </div>
            </div>

          </div>
        </section>

        {/* Main Report Grid */}
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">

          {/* Top Candidates */}
          <section className="overflow-hidden rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)] xl:col-span-2">

            <div className="border-b border-white/10 px-5 py-4">
              <SectionTitle
                icon={<Users size={17} />}
                title="Candidate Ranking"
                description="Candidates ordered by their calculated overall match score."
              />
            </div>

            <div className="overflow-x-auto">
              <table className="w-full min-w-[850px] border-collapse">

                <thead>
                  <tr className="border-b border-white/10 bg-[#111827] text-left">
                    <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Rank
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
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
                      Semantic
                    </th>

                    <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Decision
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {sortedCandidates.map((candidate, index) => (
                    <tr
                      key={candidate.id}
                      className="border-b border-white/5 last:border-b-0 hover:bg-white/[0.03]"
                    >
                      <td className="px-5 py-4">
                        <span className="text-[12px] font-semibold text-slate-500">
                          #{index + 1}
                        </span>
                      </td>

                      <td className="px-4 py-4">
                        <div className="text-[13px] font-medium text-white">
                          {candidate.name}
                        </div>

                        <div className="mt-0.5 text-[11px] text-slate-600">
                          {candidate.role}
                        </div>
                      </td>

                      <td className="px-4 py-4">
                        <span className="text-[13px] font-semibold text-[#7EA2FF]">
                          {candidate.overallScore.toFixed(1)}%
                        </span>
                      </td>

                      <td className="px-4 py-4 text-[12px] text-slate-400">
                        {candidate.skillsScore}%
                      </td>

                      <td className="px-4 py-4 text-[12px] text-slate-400">
                        {candidate.experienceScore}%
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

          {/* Matching Analysis */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <SectionTitle
              icon={<BarChart3 size={17} />}
              title="Matching Analysis"
              description="Average score across the configured matching dimensions."
            />

            <div className="space-y-5">
              <ScoreBar
                label="Skills"
                score={averageScores.skills}
              />

              <ScoreBar
                label="Experience"
                score={averageScores.experience}
              />

              <ScoreBar
                label="Education"
                score={averageScores.education}
              />

              <ScoreBar
                label="Semantic Match"
                score={averageScores.semantic}
              />
            </div>

            <div className="mt-6 rounded-lg border border-white/10 bg-[#111827] p-4">
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                Weighted Model
              </div>

              <div className="mt-3 grid grid-cols-2 gap-3 text-[11px]">
                <div className="text-slate-400">
                  Skills <span className="float-right text-white">40%</span>
                </div>

                <div className="text-slate-400">
                  Experience <span className="float-right text-white">25%</span>
                </div>

                <div className="text-slate-400">
                  Education <span className="float-right text-white">15%</span>
                </div>

                <div className="text-slate-400">
                  Semantic <span className="float-right text-white">20%</span>
                </div>
              </div>
            </div>
          </section>

          {/* Employer Requirements */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <SectionTitle
              icon={<ShieldCheck size={17} />}
              title="Employer Requirements"
              description="Requirements supplied for the active position."
            />

            <div className="space-y-5">

              <div>
                <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                  Required Skills
                </div>

                <div className="flex flex-wrap gap-2">
                  {activeJob.requiredSkills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-md border border-[#4F7CFF]/20 bg-[#4F7CFF]/10 px-2.5 py-1.5 text-[11px] font-medium text-[#A9BEFF]"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                  Preferred Skills
                </div>

                <div className="flex flex-wrap gap-2">
                  {activeJob.preferredSkills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-md border border-white/10 bg-white/[0.03] px-2.5 py-1.5 text-[11px] text-slate-400"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">

                <div className="rounded-lg border border-white/10 bg-[#111827] p-3">
                  <div className="text-[10px] text-slate-600">
                    Minimum Experience
                  </div>

                  <div className="mt-2 text-[13px] font-medium text-white">
                    {activeJob.minimumExperienceMonths} months
                  </div>
                </div>

                <div className="rounded-lg border border-white/10 bg-[#111827] p-3">
                  <div className="text-[10px] text-slate-600">
                    Education
                  </div>

                  <div className="mt-2 text-[13px] font-medium text-white">
                    {activeJob.education}
                  </div>
                </div>

              </div>

            </div>
          </section>

          {/* Requirement Gaps */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)] xl:col-span-2">

            <SectionTitle
              icon={<Target size={17} />}
              title="Requirement Gap Analysis"
              description="Areas identified by the matching engine that may require recruiter review."
            />

            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">

              {sortedCandidates.map((candidate) => (
                <div
                  key={candidate.id}
                  className="rounded-lg border border-white/10 bg-[#111827] p-4"
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <div className="text-[12px] font-medium text-white">
                        {candidate.name}
                      </div>

                      <div className="mt-1 text-[10px] text-slate-600">
                        {candidate.overallScore.toFixed(1)}% overall match
                      </div>
                    </div>

                    <span
                      className={`h-2 w-2 rounded-full ${
                        candidate.gaps.length === 0
                          ? 'bg-emerald-400'
                          : 'bg-amber-400'
                      }`}
                    />
                  </div>

                  <div className="mt-3 space-y-2">
                    {candidate.gaps.map((gap) => (
                      <div
                        key={gap}
                        className="text-[11px] leading-5 text-slate-500"
                      >
                        {gap}
                      </div>
                    ))}
                  </div>
                </div>
              ))}

            </div>
          </section>

          {/* Decision Framework */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)] xl:col-span-2">

            <SectionTitle
              icon={<ShieldCheck size={17} />}
              title="Decision Framework"
              description="Configured rules used to produce matching outcomes."
            />

            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">

              <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
                <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                  Overall Threshold
                </div>

                <div className="mt-3 text-[24px] font-semibold text-white">
                  70%
                </div>

                <p className="mt-2 text-[11px] leading-5 text-slate-500">
                  Minimum configured overall match score.
                </p>
              </div>

              <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
                <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                  Mandatory Requirements
                </div>

                <div className="mt-3 flex items-center gap-2 text-[14px] font-semibold text-emerald-300">
                  <CheckCircle2 size={16} />
                  Required
                </div>

                <p className="mt-2 text-[11px] leading-5 text-slate-500">
                  Mandatory employer requirements must be satisfied.
                </p>
              </div>

              <div className="rounded-lg border border-white/10 bg-[#111827] p-4">
                <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-600">
                  Semantic Threshold
                </div>

                <div className="mt-3 text-[24px] font-semibold text-white">
                  75%
                </div>

                <p className="mt-2 text-[11px] leading-5 text-slate-500">
                  Minimum semantic similarity configured for qualification.
                </p>
              </div>

            </div>

            <div className="mt-5 border-t border-white/10 pt-4">
              <p className="text-[10px] leading-5 text-slate-600">
                MeritMatch provides decision-support information based on
                employer-defined requirements. Recruitment decisions remain
                with the authorized human decision-maker.
              </p>
            </div>

          </section>

        </div>
      </div>
    </main>
  )
}
