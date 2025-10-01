export interface Profile {
  id: string
  description: string | null
  work_experiences: WorkExperience[]
}

export interface WorkExperience {
  id: string
  company_id: string | null
  company_name: string
  position: string
  description: string
  start_date: number | null
  end_date: number | null
}
