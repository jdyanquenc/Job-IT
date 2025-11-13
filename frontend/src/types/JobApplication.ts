import type { EmploymentType } from './EmploymentType'

export interface JobApplication {
  id: string
  job_title: string
  job_short_description: string | null
  experience: string
  remote: boolean
  employment_type: EmploymentType
  tags: [string]
  salary_min: string
  salary_max: string
  currency_code: string
  has_applied: boolean
  created_at: Date
  updated_at: Date | null
  expires_at: Date | null
  location: string
  country_code: string
  company_name: string
  company_image_url: string | null
  similarity_score: number | null
}
