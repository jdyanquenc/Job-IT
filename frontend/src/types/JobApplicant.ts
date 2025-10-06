export interface JobApplicant {
  job_id: string
  user_id: string
  status: string
  applied_at: number

  first_name: string
  last_name: string
  title: string
  description: string
  skills: string[]
  location: string
  photo_url: string
}
