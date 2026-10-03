import {
  AlertCircle,
  CheckCircle2,
  FileText,
  Loader2,
  Upload,
  UserRound,
} from 'lucide-react'
import { useState } from 'react'
import { matchCandidate, parseResume } from '../services/api'

type MatchResult = {
  candidate_name?: string
  job_title?: string
  scoring?: {
    overall_score?: number
    component_scores?: {
      skills?: number
      experience?: number
      education?: number
      semantic?: number
    }
  }
  decision?: {
    decision?: string
    eligible?: boolean
    reasons?: string[]
  }
  explanation?: {
    strengths?: string[]
    gaps?: string[]
  }
}

const pythonDeveloperJob = {
  job_title: 'Python Developer',
  department: 'Information Technology',
  description:
    'Develop and maintain Python applications and REST APIs.',
  required_skills: ['Python', 'SQL'],
  preferred_skills: ['FastAPI', 'PostgreSQL'],
  minimum_experience_months: 24,
  education_requirements: ['BSc Computer Science'],
}

export default function Evaluate() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<MatchResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleEvaluate() {
    if (!file) {
      setError('Please select a resume first.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const parsed = await parseResume(file)

      const match = await matchCandidate(
        parsed.profile,
        pythonDeveloperJob,
      )

      setResult(match as MatchResult)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Candidate evaluation failed.',
      )
    } finally {
      setLoading(false)
    }
  }

  const score = result?.scoring?.overall_score ?? 0
  const decision = result?.decision?.decision ?? ''

  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1200px]">

        <div className="mb-7">
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
            Candidate Evaluation
          </div>

          <h1 className="text-[28px] font-semibold tracking-tight text-white">
            Evaluate Candidate
          </h1>

          <p className="mt-2 text-[14px] text-slate-400">
            Upload a resume and evaluate the candidate against employer-defined job requirements.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[420px_1fr]">

          {/* Upload Panel */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] p-6 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            <div className="mb-5 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                <Upload size={18} />
              </div>

              <div>
                <h2 className="text-[15px] font-semibold text-white">
                  Resume Upload
                </h2>

                <p className="text-[11px] text-slate-500">
                  PDF, DOCX or TXT
                </p>
              </div>
            </div>

            <label className="flex min-h-[190px] cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-white/15 bg-[#0B1220] px-6 text-center transition hover:border-[#4F7CFF]/50 hover:bg-[#111827]">
              <FileText size={28} className="mb-3 text-slate-500" />

              <span className="text-[13px] font-medium text-slate-300">
                {file ? file.name : 'Choose a resume'}
              </span>

              <span className="mt-1 text-[11px] text-slate-600">
                Click to browse files
              </span>

              <input
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={(event) => {
                  setFile(event.target.files?.[0] ?? null)
                  setResult(null)
                  setError('')
                }}
              />
            </label>

            <div className="mt-5 rounded-lg border border-white/10 bg-[#111827] p-4">
              <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                Evaluation Target
              </div>

              <div className="mt-2 flex items-center gap-2">
                <UserRound size={15} className="text-[#7EA2FF]" />
                <span className="text-[13px] font-medium text-white">
                  Python Developer
                </span>
              </div>

              <div className="mt-1 text-[11px] text-slate-500">
                Information Technology · Remote · Full-time
              </div>
            </div>

            <button
              type="button"
              onClick={handleEvaluate}
              disabled={loading || !file}
              className="mt-5 flex h-11 w-full items-center justify-center gap-2 rounded-lg bg-[#356AE6] text-[12px] font-semibold text-white transition hover:bg-[#4577F0] disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Evaluating...
                </>
              ) : (
                <>
                  <CheckCircle2 size={16} />
                  Evaluate Candidate
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 flex items-start gap-2 rounded-lg border border-red-400/20 bg-red-400/5 p-3 text-[11px] text-red-300">
                <AlertCircle size={15} className="mt-0.5 shrink-0" />
                {error}
              </div>
            )}
          </section>

          {/* Results */}
          <section className="rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

            {!result ? (
              <div className="flex min-h-[520px] flex-col items-center justify-center px-8 text-center">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-[#243A68] text-[#7EA2FF]">
                  <UserRound size={24} />
                </div>

                <h2 className="mt-5 text-[16px] font-semibold text-white">
                  Awaiting Candidate
                </h2>

                <p className="mt-2 max-w-[420px] text-[12px] leading-6 text-slate-500">
                  Upload a resume to run the MeritMatch extraction,
                  matching, scoring and qualification pipeline.
                </p>
              </div>
            ) : (
              <>
                <div className="border-b border-white/10 p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                        Evaluation Result
                      </div>

                      <h2 className="mt-2 text-[19px] font-semibold text-white">
                        {result.candidate_name || 'Candidate'}
                      </h2>

                      <p className="mt-1 text-[11px] text-slate-500">
                        {result.job_title || 'Python Developer'}
                      </p>
                    </div>

                    <div
                      className={`rounded-full border px-3 py-1.5 text-[10px] font-semibold ${
                        decision === 'QUALIFIED'
                          ? 'border-emerald-400/20 bg-emerald-400/10 text-emerald-300'
                          : 'border-amber-400/20 bg-amber-400/10 text-amber-300'
                      }`}
                    >
                      {decision || 'REVIEW'}
                    </div>
                  </div>

                  <div className="mt-6">
                    <div className="text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Overall Match
                    </div>

                    <div className="mt-1 text-[42px] font-semibold tracking-tight text-white">
                      {score.toFixed(2)}%
                    </div>
                  </div>
                </div>

                <div className="border-b border-white/10 p-6">
                  <div className="mb-5 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Match Breakdown
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    {[
                      ['Skills', result.scoring?.component_scores?.skills],
                      ['Experience', result.scoring?.component_scores?.experience],
                      ['Education', result.scoring?.component_scores?.education],
                      ['Semantic', result.scoring?.component_scores?.semantic],
                    ].map(([label, value]) => (
                      <div
                        key={String(label)}
                        className="rounded-lg border border-white/10 bg-[#111827] p-4"
                      >
                        <div className="text-[10px] text-slate-500">
                          {label}
                        </div>

                        <div className="mt-2 text-[20px] font-semibold text-white">
                          {Number(value ?? 0).toFixed(1)}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-6 p-6 md:grid-cols-2">
                  <div>
                    <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Strengths
                    </div>

                    <div className="space-y-2">
                      {(result.explanation?.strengths ?? []).map(
                        (strength) => (
                          <div
                            key={strength}
                            className="flex gap-2 text-[11px] text-slate-400"
                          >
                            <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
                            {strength}
                          </div>
                        ),
                      )}
                    </div>
                  </div>

                  <div>
                    <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                      Requirement Gaps
                    </div>

                    <div className="space-y-2">
                      {(result.explanation?.gaps ?? []).length > 0 ? (
                        result.explanation?.gaps?.map((gap) => (
                          <div
                            key={gap}
                            className="flex gap-2 text-[11px] text-slate-400"
                          >
                            <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-400" />
                            {gap}
                          </div>
                        ))
                      ) : (
                        <div className="text-[11px] text-emerald-300">
                          No requirement gaps identified.
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </>
            )}
          </section>
        </div>
      </div>
    </main>
  )
}
