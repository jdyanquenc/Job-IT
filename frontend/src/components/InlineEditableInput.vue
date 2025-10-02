<script setup lang="ts">
import { ref, watch } from 'vue'
import { NInput, NButton } from 'naive-ui'

interface Props {
    modelValue: string
    label?: string
    placeholder?: string
    type?: 'textarea' | 'text'
}

const props = withDefaults(defineProps<Props>(), {
    type: 'textarea'
})
const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
    (e: 'save', value: string): void
}>()



const editing = ref(false)
const tempValue = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
    if (!editing.value) {
        tempValue.value = newVal
    }
})

function startEditing() {
    tempValue.value = props.modelValue
    editing.value = true
}

function cancelEdit() {
    editing.value = false
    tempValue.value = props.modelValue
}

function saveEdit() {
    editing.value = false
    emit('update:modelValue', tempValue.value)
    emit('save', tempValue.value)
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
        e.preventDefault()
        saveEdit()
    }
}
</script>

<template>
    <div class="w-full mb-4">
        <h5 v-if="label">{{ label }}</h5>

        <!-- Vista lectura -->
        <div v-if="!editing" @click="startEditing" class="cursor-pointer">
            <article class="prose prose-gray">
                <p v-if="modelValue" title="Haz clic para editar">
                    {{ modelValue }}
                </p>
                <p v-else class="text-gray-400 italic">
                    {{ placeholder || 'Haz clic para agregar contenido' }}
                </p>
            </article>
        </div>

        <!-- Vista edición -->
        <div v-else>
            <n-input v-model:value="tempValue" :type="props.type" :rows="props.type === 'textarea' ? 4 : undefined"
                autofocus :placeholder="placeholder || 'Escribe aquí...'"
                v-on="props.type !== 'textarea' ? { keydown: handleKeydown } : {}" />
            <div class="flex justify-end gap-2 mt-2">
                <n-button size="small" tertiary @click="cancelEdit">Cancelar</n-button>
                <n-button size="small" type="primary" @click="saveEdit">Guardar</n-button>
            </div>
        </div>
    </div>
</template>
