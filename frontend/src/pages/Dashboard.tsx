import { useState } from 'react'
import MetricCard from '../components/dashboard/MetricCard'
import CandidateTable from '../components/dashboard/CandidateTable'
import CandidateOverview from '../components/dashboard/CandidateOverview'
import { candidates } from '../data/demoData'
import type { Candidate } from '../types/meritmatch'

export default function Dashboard() {
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate>(
    candidates[0],
  )

  return (
    <main className="flex-1 overflow-auto bg-[#0F172A] p-8">
      <div className="mx-auto max-w-[1440px]">
        <div className="mb-8">
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.18em] text-[#7EA2FF]">
            Candidate Intelligence
          </div>

          <div className="flex items-start justify-between gap-6">
            <div>
              <h1 className="text-[30px] font-semibold tracking-tight text-white">
                Recruitment workspace
              </h1>

              <p className="mt-2 text-[14px] text-slate-400">
                Evaluate candidates against employer-defined requirements.
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-[12px] font-medium text-emerald-300">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              Matching engine ready
            </div>
          </div>
        </div>

        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            label="Candidates"
            value="24"
            detail="Candidates in workspace"
          />

          <MetricCard
            label="Qualified"
            value="18"
            detail="Meeting current requirements"
            accent="#34D399"
          />

          <MetricCard
            label="Average Match"
            value="86.7%"
            detail="Across evaluated candidates"
            accent="#7EA2FF"
          />

          <MetricCard
            label="Active Job"
            value="01"
            detail="Python Developer"
            accent="#F5B942"
          />
        </section>

        <div className="mt-6">
          <CandidateTable
            candidates={candidates}
            selectedCandidateId={selectedCandidate.id}
            onSelectCandidate={setSelectedCandidate}
          />
        </div>

        <div className="mt-6">
          <CandidateOverview candidate={selectedCandidate} />
        </div>
      </div>
    </main>
  )
}
