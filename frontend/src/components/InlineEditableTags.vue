<script setup lang="ts">
import { ref, watch } from "vue";
import { NButton, NDynamicTags, NTag, NPopover } from "naive-ui";

interface Props {
    modelValue: string[];
    label?: string;
    placeholder?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(["update:modelValue"]);

const editing = ref(false);
const tempValue = ref(Array.isArray(props.modelValue) ? [...props.modelValue] : []);

watch(() => props.modelValue, (newVal) => {
    if (!editing.value) {
        tempValue.value = Array.isArray(newVal) ? [...newVal] : [];
    }
});

function startEditing() {
    tempValue.value = Array.isArray(props.modelValue) ? [...props.modelValue] : [];
    editing.value = true;
}

function cancelEdit() {
    editing.value = false;
    tempValue.value = Array.isArray(props.modelValue) ? [...props.modelValue] : [];
}

function saveEdit() {
    editing.value = false;
    emit("update:modelValue", tempValue.value);
}

</script>

<template>
    <div class="w-full mb-4">
        <h5 v-if="label">{{ label }}</h5>

        <!-- Vista lectura -->
        <div v-if="!editing" @click="startEditing" class="cursor-pointer">
            <article v-if="modelValue && modelValue.length">
                <NTag v-for="(tag, index) in modelValue" :key="index" size="large" type="success" spacing="small"
                    class="m-1">
                    {{ tag }}
                </NTag>
            </article>
            <span v-else class="text-gray-400 italic">
                {{ placeholder || "Sin etiquetas" }}
            </span>
        </div>

        <!-- Vista edición -->
        <div v-else>
            <NDynamicTags v-model:value="tempValue" :placeholder="placeholder || 'Agrega una etiqueta y presiona Enter'"
                size="medium" />

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
