export type CandidateStatus = 'Qualified' | 'Review' | 'Not Qualified'

export type Candidate = {
  id: string
  name: string
  role: string
  overallScore: number
  skillsScore: number
  experienceScore: number
  educationScore: number
  semanticScore: number
  experienceMonths: number
  status: CandidateStatus
  strengths: string[]
  gaps: string[]
}

export type Job = {
  id: string
  title: string
  department: string
  location: string
  workArrangement: string
  employmentType: string
  requiredSkills: string[]
  preferredSkills: string[]
  minimumExperienceMonths: number
  education: string
}
