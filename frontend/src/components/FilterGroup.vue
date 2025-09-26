<script setup>
import { ref, watch } from "vue"
import { NCheckboxGroup, NCheckbox, NTag } from "naive-ui"

// Props
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    options: {
        type: Array,
        required: true,
    },
    showAllOption: {
        type: Boolean,
        default: true
    },
    allOptionLabel: {
        type: String,
        default: "All"
    },
    modelValue: {
        type: Array,
        default: () => []
    }
})

// Emitir cambios al padre
const emit = defineEmits(["update:modelValue", "update:allOption"])

// Estado local
const selected = ref([...new Set([...props.modelValue])])
const allSelected = ref(false)


const toogleAll = () => {
    if (allSelected.value === false) {
        selected.value = []
    } else {
        selected.value = props.options.map(opt => opt.id)
    }

    // Emitir el nuevo valor al padre
    emit("update:modelValue", selected.value)
    emit("update:allOption", allSelected.value)
}

// Manejar cambios de selección
const handleChange = (values) => {
    // Eliminar duplicados y actualizar el modelo
    selected.value = [...new Set(values)]

    // Actualizar el estado de "All" basado en la selección actual
    allSelected.value = selected.value.length === props.options.length

    // Emitir el nuevo valor al padre
    emit("update:modelValue", selected.value)
    emit("update:allOption", allSelected.value)
}

// Sincronizar con valor externo
watch(
    () => props.modelValue,
    (newVal) => {
        selected.value = [...new Set(newVal)]
    }

)
</script>

<template>
    <div class="bg-white rounded-md p-4">
        <h3 class="font-semibold text-lg text-gray-800 mb-4">{{ title }}</h3>

        <div v-if="showAllOption" class="flex items-center justify-between mb-3">
            <n-checkbox v-model:checked="allSelected" @update:checked="toogleAll">
                {{ allOptionLabel }}
            </n-checkbox>
            <n-tag round size="small" :bordered="false" type="info" class="shadow !bg-green-100 !text-green-600">
                {{options.map(opt => opt.count).reduce((a, b) => a + b, 0)}}
            </n-tag>
        </div>

        <n-checkbox-group v-model:value="selected" @update:value="handleChange">

            <div v-for="item in options" :key="item.id" class="flex items-center justify-between mb-3">
                <n-checkbox :value="item.id">
                    {{ item.name }}
                </n-checkbox>

                <n-tag round size="small" :bordered="false" type="info" class="shadow !bg-green-100 !text-green-600">
                    {{ item.count }}
                </n-tag>
            </div>
        </n-checkbox-group>
    </div>
</template>
