import type { MessageProviderInst } from 'naive-ui'

let messageProvider: MessageProviderInst | null = null

export function setMessageProvider(inst: MessageProviderInst) {
  messageProvider = inst
}

export function getMessageProvider() {
  if (!messageProvider) {
    console.warn('Message provider instance not set')
  }
  return messageProvider
}
