export function timeAgo(isoDate: string): string {
  const date = new Date(isoDate)

  if (isNaN(date.getTime())) {
    return 'Fecha inválida'
  }

  const now = new Date()

  const diffMs = now.getTime() - date.getTime()
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  if (diffSec < 60) return `Hace ${diffSec} segundo${diffSec === 1 ? '' : 's'}`
  if (diffMin < 60) return `Hace ${diffMin} minuto${diffMin === 1 ? '' : 's'}`
  if (diffHour < 24) return `Hace ${diffHour} hora${diffHour === 1 ? '' : 's'}`
  if (diffDay < 7) return `Hace ${diffDay} día${diffDay === 1 ? '' : 's'}`

  // fallback for older dates
  return date.toLocaleDateString()
}
