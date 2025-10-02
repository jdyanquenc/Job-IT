<script setup lang="ts">
import { ref } from "vue"
import { NInput, NButton } from "naive-ui"
import { useProfileStore } from "@/stores"
import { useRoute } from "vue-router"


const route = useRoute()
const profileStore = useProfileStore()

const id = route.params.id

const editing = ref(false)
const tempValue = ref(profileStore.profile.description || "")

function startEditing() {
    tempValue.value = profileStore.profile.description || ""
    editing.value = true
}

async function saveEdit() {
    editing.value = false
    await profileStore.updateDescription(tempValue.value)
}

function cancelEdit() {
    editing.value = false
    tempValue.value = profileStore.profile.description || ""
}

profileStore.load(id as string)

</script>


<template>
    <div class="w-full mb-4">
        <h5>Acerca de Mi</h5>
        <!-- Si no está en edición -->
        <div v-if="!editing" @click="startEditing" class="cursor-pointer">
            <article class="prose prose-gray">
                <p v-if="profileStore.profile.description" title="Haz clic para editar">
                    {{ profileStore.profile.description }}
                </p>
                <p v-else class="text-gray-400 italic">Cuéntanos sobre ti, tu perfil profesional y tus metas. Haz clic
                    para editar</p>
            </article>
        </div>
        <!-- Vista edición -->
        <div v-else>
            <n-input v-model:value="tempValue" type="textarea" rows="4" autofocus placeholder="Escribe aquí..." />

            <!-- Botones en fila aparte -->
            <div class="flex justify-end gap-2 mt-2">
                <n-button size="small" tertiary @click="cancelEdit">Cancelar</n-button>
                <n-button size="small" type="primary" @click="saveEdit">Guardar</n-button>
            </div>
        </div>
    </div>
</template>
