export interface RegisterUser {
  identification_type: string | null
  identification_number: string | null
  first_name: string | null
  last_name: string | null
  email: string | null
  password: string | null
  confirm_password: string | null
}

export interface UserCredentials {
  email: string
  password: string
}

export interface User {
  id: number
  firstName: string
  lastName: string
  email: string
  password?: string // Optional for security reasons
  isDeleting?: boolean // Optional for UI purposes
}
