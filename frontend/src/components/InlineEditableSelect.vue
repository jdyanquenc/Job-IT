<script setup lang="ts">
import { ref, watch } from "vue";
import { NButton, NSelect, NPopover } from "naive-ui";

interface Option {
    label: string;
    value: string | number;
}

interface Props {
    modelValue: string;
    label?: string;
    placeholder?: string;
    options: Option[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
    (e: 'save', value: string): void
}>()

const editing = ref(false);
const tempValue = ref(props.modelValue);

watch(() => props.modelValue, (newVal) => {
    if (!editing.value) {
        tempValue.value = newVal
    }
})

function startEditing() {
    tempValue.value = props.modelValue;
    editing.value = true;
}

function cancelEdit() {
    editing.value = false;
    tempValue.value = props.modelValue;
}

function saveEdit() {
    editing.value = false;
    emit("update:modelValue", tempValue.value);
    emit('save', tempValue.value)
}



</script>

<template>
    <div class="w-full mb-4">
        <h5 v-if="label">{{ label }}</h5>

        <!-- Vista normal -->
        <div v-if="!editing" @click="startEditing" class="cursor-pointer">
            <article class="prose prose-gray">
                <p v-if="modelValue" title="Haz clic para editar">
                    {{props.options.find(o => o.value === props.modelValue)?.label || props.placeholder ||
                        "Selecciona una opción"}}
                </p>
                <p v-else class="text-gray-400 italic">
                    {{ placeholder || 'Haz clic para seleccionar una opción' }}
                </p>
            </article>
        </div>

        <!-- Vista edición -->
        <div v-else>
            <NSelect v-model:value="tempValue" :options="props.options as any"
                :placeholder="props.placeholder || 'Selecciona una opción'" style="min-width: 180px" />
            <div class="flex justify-end gap-2 mt-2">
                <n-popover trigger="hover">
                    <template #trigger>
                        <n-button size="tiny" ghost @click="saveEdit">✔</n-button>
                    </template>
                    <span>Guardar cambios</span>
                </n-popover>
                <n-popover trigger="hover">
                    <template #trigger>
                        <n-button size="tiny" ghost @click="cancelEdit">✖</n-button>
                    </template>
                    <span>Cancelar edición</span>
                </n-popover>
            </div>
        </div>
    </div>
</template>
