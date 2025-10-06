export interface Profile {
  id: string
  full_name: string
  title: string
  description: string
  location: string
  salary_range: string
  modality: string
  education_experiences: EducationExperience[]
  work_experiences: WorkExperience[]
  skills: string[]
  photo_url: string | null
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

export interface EducationExperience {
  id: string
  institution_id: string | null
  institution_name: string
  degree: string
  field_of_study: string
  start_date: number | null
  end_date: number | null
}
