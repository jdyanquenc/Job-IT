export type EmploymentType = 'Full-time' | 'Part-time' | 'Contract';

export interface CompanyBasicInfo {
  id: string | null
  name: string
  location: string
  country_code: string
  logo_url: string | null
}

export interface Job {
  id: string
  job_title: string
  job_short_description: string | null
  experience: string
  remote: boolean
  employment_type: EmploymentType
  tags: [string]
  salary_range: string
  created_at: Date 
  updated_at: Date | null
  expires_at: Date | null
  company: CompanyBasicInfo
}

export interface JobDetail {
  id: string
  job_title: string
  job_description: string
  responsibilities: string
  skills: string
  benefits: string
  experience: string
  remote: boolean
  employment_type: EmploymentType
  tags: []
  salary_range: string
  created_at: Date 
  updated_at: Date | null
  expires_at: Date | null
}

export interface RegisterJob extends Omit<JobDetail, 'id' | 'created_at' | 'updated_at'> {
  location: string
  country_code: string
}