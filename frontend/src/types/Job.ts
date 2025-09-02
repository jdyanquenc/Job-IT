export interface RegisterJob {
  firstName: string | null
  lastName: string | null
  username: string | null
  password: string | null
}

export interface Job {
  id: string
  job_title: string
  job_short_description: string
  remote: boolean
  employment_type: EmploymentType
  skills_required: [string]
  salary_range: string
  created_at: Date 
  updated_at: Date | null
  expires_at: Date | null
  company: CompanyBasicInfo
}

export interface CompanyBasicInfo {
  id: string | null
  name: string
  location: string
  country_code: string
  logo_url: string | null
}

export type EmploymentType = 'Full-time' | 'Part-time' | 'Contract';

