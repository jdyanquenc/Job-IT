import type { LoadingBarProviderInst } from 'naive-ui'

let loadingBar: LoadingBarProviderInst | null = null

export function setLoadingBar(inst: LoadingBarProviderInst) {
  loadingBar = inst
}

export function getLoadingBar() {
  if (!loadingBar) {
    console.warn('>>>> Loading bar instance not set')
  }
  return loadingBar
}
