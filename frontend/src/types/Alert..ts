export type AlertType = 'default' | 'error' | 'info' | 'success' | 'warning'

export type Alert = { id: any; type: AlertType; title: string; message: string }
