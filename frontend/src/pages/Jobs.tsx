import { BriefcaseBusiness, MapPin, Plus, Users } from 'lucide-react'

type Job = {
  id: string
  title: string
  department: string
  location: string
  arrangement: string
  employmentType: string
  candidates: number
  matches: number
  status: 'Active' | 'Draft' | 'Closed'
}

const jobs: Job[] = [
  {
    id: 'job-001',
    title: 'Python Developer',
    department: 'Information Technology',
    location: 'Remote',
    arrangement: 'Remote',
    employmentType: 'Full-time',
    candidates: 24,
    matches: 18,
    status: 'Active',
  },
  {
    id: 'job-002',
    title: 'Data Analyst',
    department: 'Data & Analytics',
    location: 'Johannesburg',
    arrangement: 'Hybrid',
    employmentType: 'Full-time',
    candidates: 16,
    matches: 11,
    status: 'Active',
  },
  {
    id: 'job-003',
    title: 'Software Engineer',
    department: 'Engineering',
    location: 'Cape Town',
    arrangement: 'Hybrid',
    employmentType: 'Full-time',
    candidates: 31,
    matches: 21,
    status: 'Active',
  },
  {
    id: 'job-004',
    title: 'Business Analyst',
    department: 'Operations',
    location: 'Remote',
    arrangement: 'Remote',
    employmentType: 'Contract',
    candidates: 9,
    matches: 5,
    status: 'Draft',
  },
]

const statusStyles = {
  Active: 'border-emerald-400/20 bg-emerald-400/10 text-emerald-300',
  Draft: 'border-white/10 bg-white/5 text-slate-400',
  Closed: 'border-red-400/20 bg-red-400/10 text-red-300',
}

export default function Jobs() {
  return (
    <main className="flex-1 overflow-auto bg-[#0B1220] p-8">
      <div className="mx-auto max-w-[1440px]">

        {/* Page Header */}
        <div className="mb-8 flex items-start justify-between gap-6">
          <div>
            <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7EA2FF]">
              Job Management
            </div>

            <h1 className="text-[28px] font-semibold tracking-tight text-white">
              Jobs
            </h1>

            <p className="mt-2 text-[14px] text-slate-400">
              Define and manage employer-specific requirements for each position.
            </p>
          </div>

          <button
            type="button"
            className="flex items-center gap-2 rounded-lg bg-[#356AE6] px-4 py-2.5 text-[12px] font-semibold text-white shadow-[0_6px_18px_rgba(53,106,230,0.25)] transition hover:bg-[#4377F0]"
          >
            <Plus size={16} strokeWidth={2} />
            Create Job
          </button>
        </div>

        {/* Summary Metrics */}
        <section className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] font-medium text-slate-400">
              <BriefcaseBusiness size={16} className="text-[#7EA2FF]" />
              Total Jobs
            </div>

            <div className="mt-3 text-[27px] font-semibold tracking-tight text-white">
              {jobs.length}
            </div>

            <div className="mt-1 text-[11px] text-slate-500">
              Positions in workspace
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] font-medium text-slate-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              Active Jobs
            </div>

            <div className="mt-3 text-[27px] font-semibold tracking-tight text-white">
              {jobs.filter((job) => job.status === 'Active').length}
            </div>

            <div className="mt-1 text-[11px] text-slate-500">
              Currently accepting candidates
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#151F33] p-5 shadow-[0_8px_24px_rgba(0,0,0,0.18)]">
            <div className="flex items-center gap-2 text-[12px] font-medium text-slate-400">
              <Users size={16} className="text-[#7EA2FF]" />
              Candidates
            </div>

            <div className="mt-3 text-[27px] font-semibold tracking-tight text-white">
              {jobs.reduce((total, job) => total + job.candidates, 0)}
            </div>

            <div className="mt-1 text-[11px] text-slate-500">
              Across all job positions
            </div>
          </div>

        </section>

        {/* Jobs Table */}
        <section className="overflow-hidden rounded-xl border border-white/10 bg-[#151F33] shadow-[0_8px_24px_rgba(0,0,0,0.18)]">

          <div className="border-b border-white/10 px-5 py-4">
            <h2 className="text-[15px] font-semibold text-white">
              Job Positions
            </h2>

            <p className="mt-1 text-[11px] text-slate-500">
              Employer-defined positions available for candidate matching
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[900px] border-collapse">

              <thead>
                <tr className="border-b border-white/10 bg-[#111827] text-left">

                  <th className="px-5 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Position
                  </th>

                  <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Location
                  </th>

                  <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Type
                  </th>

                  <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Candidates
                  </th>

                  <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Matches
                  </th>

                  <th className="px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500">
                    Status
                  </th>

                </tr>
              </thead>

              <tbody>

                {jobs.map((job) => (
                  <tr
                    key={job.id}
                    className="cursor-pointer border-b border-white/5 transition last:border-b-0 hover:bg-white/[0.03]"
                  >

                    <td className="px-5 py-4">

                      <div className="flex items-center gap-3">

                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#243A68] text-[#7EA2FF]">
                          <BriefcaseBusiness size={16} />
                        </div>

                        <div>

                          <div className="text-[13px] font-medium text-white">
                            {job.title}
                          </div>

                          <div className="mt-0.5 text-[11px] text-slate-500">
                            {job.department}
                          </div>

                        </div>

                      </div>

                    </td>

                    <td className="px-4 py-4">

                      <div className="flex items-center gap-1.5 text-[12px] text-slate-400">
                        <MapPin size={14} />
                        {job.location}
                      </div>

                      <div className="mt-1 text-[10px] text-slate-600">
                        {job.arrangement}
                      </div>

                    </td>

                    <td className="px-4 py-4 text-[12px] text-slate-400">
                      {job.employmentType}
                    </td>

                    <td className="px-4 py-4 text-[12px] font-medium text-white">
                      {job.candidates}
                    </td>

                    <td className="px-4 py-4 text-[12px] font-medium text-[#7EA2FF]">
                      {job.matches}
                    </td>

                    <td className="px-4 py-4">

                      <span
                        className={`inline-flex rounded-full border px-2.5 py-1 text-[11px] font-medium ${statusStyles[job.status]}`}
                      >
                        {job.status}
                      </span>

                    </td>

                  </tr>
                ))}

              </tbody>

            </table>
          </div>

        </section>

      </div>
    </main>
  )
}
