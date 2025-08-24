<script setup lang="ts">

import { NButton } from 'naive-ui'
import { useDialog } from 'naive-ui'

const dialog = useDialog()

function showDialog() {
  dialog.warning({
    title: 'Warning',
    content: 'Are you sure you want to continue?',
    positiveText: 'Yes',
    negativeText: 'No',
    onPositiveClick: () => {
      console.log('User clicked Yes')
    },
    onNegativeClick: () => {
      console.log('User clicked No')
    }
  })
}


</script>

<template>
  <div>
    <n-button @click="showDialog">Open Dialog</n-button>

  </div>
</template>
