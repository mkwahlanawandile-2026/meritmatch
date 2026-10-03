const API_BASE_URL =
  import.meta.env.VITE_API_URL?.replace(/\/$/, '') ||
  'http://localhost:8000'

export type ResumeParseResponse = {
  filename: string
  profile: Record<string, unknown>
}

export type MatchResponse = Record<string, unknown>

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = `API request failed (${response.status})`

    try {
      const error = await response.json()

      if (typeof error.detail === 'string') {
        message = error.detail
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json() as Promise<T>
}

export async function checkApiHealth(): Promise<{
  status: string
  service: string
  version: string
}> {
  const response = await fetch(`${API_BASE_URL}/health`)
  return handleResponse(response)
}

export async function parseResume(
  file: File,
): Promise<ResumeParseResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(
    `${API_BASE_URL}/api/resumes/parse`,
    {
      method: 'POST',
      body: formData,
    },
  )

  return handleResponse<ResumeParseResponse>(response)
}

export async function matchCandidate(
  candidateProfile: Record<string, unknown>,
  jobRequirements: Record<string, unknown>,
): Promise<MatchResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/match`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        candidate_profile: candidateProfile,
        job_requirements: jobRequirements,
      }),
    },
  )

  return handleResponse<MatchResponse>(response)
}
