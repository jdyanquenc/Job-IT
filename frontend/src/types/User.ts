export interface RegisterUser {
  firstName: string | null
  lastName: string | null
  email: string | null
  password: string | null
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
