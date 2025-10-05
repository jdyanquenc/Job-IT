/* eslint-disable @typescript-eslint/no-explicit-any */
import { useDialog, useMessage } from 'naive-ui'
import { useJobsStore } from '@/stores'

export function useJobApplication() {
  const dialog = useDialog()
  const message = useMessage()
  const jobsStore = useJobsStore()

  async function handleApply(jobId: string) {
    dialog.success({
      title: 'Confirmar postulación',
      content: '¿Seguro que deseas postularte a esta oferta?',
      positiveText: 'Sí, postularme',
      negativeText: 'Cancelar',
      async onPositiveClick() {
        try {
          await jobsStore.applyToJob(jobId)
          message.success('Te has postulado correctamente a la oferta.')
        } catch (error: any) {
          const msg = error?.detail || 'No se pudo completar la postulación.'
          message.error(msg)
        } finally {
          dialog.destroyAll()
        }
      },
    })
  }

  return {
    handleApply,
  }
}
