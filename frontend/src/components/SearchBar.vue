<script setup>
import { ref, watch } from "vue"
import { NInput, NButton, NIcon } from "naive-ui"

const modelValue = defineModel({ type: String, default: "" })

const props = defineProps({
    placeholder: { type: String, default: "" }
})

const emit = defineEmits(["search"])

const keyword = ref(modelValue.value)

function search() {
    modelValue.value = keyword.value
    emit("search", keyword.value)
}

watch(
    () => modelValue.value,
    (newVal) => {
        keyword.value = newVal
    }
)
</script>

<template>
    <div class="w-full flex justify-center">
        <div class="flex w-full max-w-2xl items-center gap-2 p-2">
            <n-input v-model:value="keyword" type="text" size="large" :placeholder="placeholder" class="shadow-md"
                @keyup.enter="search" />

            <n-button type="primary" size="large" @click="search">
                <template #icon>
                    <n-icon>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M21 21l-4.35-4.35M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z" />
                        </svg>
                    </n-icon>
                </template>
                Buscar
            </n-button>
        </div>
    </div>
</template>
