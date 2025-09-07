<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'

import { NButton, NCard, NForm, NFormItemRow, NInput, useMessage } from 'naive-ui'

import { ref } from 'vue'
import { useAuthStore } from '@/stores';
import type { UserCredentials } from '@/types';


const message = useMessage();

const isSubmitting = ref(false);

const formRef = ref<FormInst | null>(null)

const model = ref<UserCredentials>({
    username: '',
    password: ''
})

const rules: FormRules = {
    username: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    password: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    }
};

function handleValidateButtonClick(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate(
        (errors: Array<FormValidationError> | undefined) => {
            if (!errors) {
                onSubmit()
            }
            else {
                message.error('Completa los campos requeridos para continuar.')
            }
        }
    )
}

async function onSubmit() {
    const authStore = useAuthStore();
    const { username, password } = model.value;
    try {
        isSubmitting.value = true;
        await authStore.login(username, password);
    }
    catch (error: any) {
        message.error('Login failed: ' + error);
    }
    finally {
        isSubmitting.value = false;
    }
}
</script>

<template>

    <div class="max-h-screen max-w-screen-sm mx-auto mt-5 mb-5">
        <div class="flex items-center justify-center px-4">
            <div class="w-full max-w-md bg-white p-8">


                <!-- Title -->
                <h2 class="font-bold text-center text-gray-900 mb-2">Inicia sesión</h2>
                
                <p class="text-center text-gray-500 text-sm mb-6">
                    Accede a todas las características de Job IT.
                </p>


                <!-- Form -->
                <n-form ref="formRef" :model="model" :rules="rules" class="space-y-4">
                    <n-form-item-row path="username" label="Usuario">
                        <n-input v-model:value="model.username" placeholder="Steven Jobs :)" />
                    </n-form-item-row>

                    <n-form-item-row path="password" label="Contraseña">
                        <n-input v-model:value="model.password" type="password" placeholder="**********" />
                    </n-form-item-row>


                </n-form>


                <!-- Submit -->
                <n-button type="primary"
                    class="w-full bg-blue-900 text-white py-2 rounded-md hover:bg-blue-800 transition" block strong
                    @click="handleValidateButtonClick"
                    :disabled="isSubmitting || (model.username == '' || model.password == '')">
                    Iniciar sesión
                </n-button>


                <!-- Footer -->
                <p class="mt-6 text-center text-sm text-gray-500">
                    ¿Aún no tienes una cuenta?
                    <RouterLink to="/account/register" class="text-blue-600 hover:underline ml-1">Regístrate</RouterLink>
                </p>

            </div>
        </div>

        <div class="img-2 flex-clear">
            <img alt="JobBox" src="/public/images/template/login/img-3.svg">
        </div>
    </div>


</template>
