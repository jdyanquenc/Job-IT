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
    email: '',
    password: ''
})

const rules: FormRules = {
    email: {
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
    const { email, password } = model.value;
    try {
        isSubmitting.value = true;
        await authStore.login(email, password);
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
    
    
    <div class="max-w-screen-sm md:w-1/2 mx-auto mt-5 mb-5">
        <div class="flex items-center justify-center px-4">
            <div class="w-full max-w-md bg-white p-8">


                <!-- Title -->
                <h2 class="font-bold text-center text-gray-900 mb-2">Inicia sesión</h2>
                
                <p class="text-center text-gray-500 text-sm mb-6">
                    Accede a todas las características de Job IT.
                </p>


                <!-- Form -->
                <n-form ref="formRef" :model="model" :rules="rules" class="space-y-4">
                    <n-form-item-row path="email" label="Correo electronico">
                        <n-input v-model:value="model.email" placeholder="steven@job.it :)" />
                    </n-form-item-row>

                    <n-form-item-row path="password" label="Contraseña">
                        <n-input v-model:value="model.password" type="password" placeholder="**********" />
                    </n-form-item-row>

                    <!-- Submit -->
                    <n-button type="primary"
                        class="w-full text-white py-2 rounded-md" block strong
                        @click="handleValidateButtonClick"
                        :disabled="isSubmitting || (model.email == '' || model.password == '')">
                        Iniciar sesión
                    </n-button>

                </n-form>

                <!-- Footer -->
                <p class="mt-6 text-center text-sm text-gray-500">
                    ¿Aún no tienes una cuenta?
                    <RouterLink to="/account/register" class="text-blue-600 hover:underline ml-1">Regístrate</RouterLink>
                </p>

            </div>
        </div>

        <div class="hidden md:block flex justify-start mt-6 ml-6 bg-login">
        </div>
       
    </div>


</template>

<style scoped>
.bg-login {
    min-height: 200px;
    background-image: url('/public/images/template/login/img-3.svg');
    background-repeat: no-repeat;
    background-position: right center;
}
</style>
