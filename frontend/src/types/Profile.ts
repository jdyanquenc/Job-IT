export interface Profile {
  id: string
  description: string | null
  education_experiences: EducationExperience[]
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

export interface EducationExperience {
  id: string
  institution_id: string | null
  institution_name: string
  degree: string
  field_of_study: string
  start_date: number | null
  end_date: number | null
}
