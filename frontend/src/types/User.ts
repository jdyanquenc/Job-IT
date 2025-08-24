export interface RegisterUser {
  firstName: string | null
  lastName: string | null
  username: string | null
  password: string | null
}

export interface UserCredentials {
  username: string
  password: string
}

export interface User {
  id: number
  firstName: string
  lastName: string
  username: string
  password?: string // Optional for security reasons
  isDeleting?: boolean // Optional for UI purposes
}
