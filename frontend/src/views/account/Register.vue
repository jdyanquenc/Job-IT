<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'

import { NButton, NForm, NFormItem, NInput, useMessage } from 'naive-ui'

import { ref } from 'vue'
import { useUsersStore } from '@/stores';
import { router } from '@/router';
import type { RegisterUser } from '@/types';


const message = useMessage();

const isSubmitting = ref(false);

const formRef = ref<FormInst | null>(null)

const model = ref<RegisterUser>({
    firstName: null,
    lastName: null,
    email: null,
    password: null
})

const rules: FormRules = {
    documentType: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    documentNumber: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    firstName: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    lastName: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
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

function handleCompanyRegisterClick() {
    router.push('/account/company-register');
}
function handleValidateButtonClick(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate(
        (errors: Array<FormValidationError> | undefined) => {
            if (!errors) {
                onSubmit()
            }
            else {
                message.error('Verifica los campos en rojo y vuelve a intentarlo.');
            }
        }
    )
}

async function onSubmit() {
    const usersStore = useUsersStore();
    const registerUser: RegisterUser = model.value;

    try {
        isSubmitting.value = true;
        await usersStore.register(registerUser);
        await router.push('/account/login');
    }
    catch (error: any) {
        console.error('Registration failed:', error);
    }
    finally {
        isSubmitting.value = false;
    }
}

</script>

<template>

    <div class="max-w-screen-sm md:w-1/2  mx-auto mt-5 mb-5">
        <div class="flex flex-col justify-between items-center px-4">
            <div class="w-full p-8">

                <!-- Title -->
                <h2 class="font-bold text-center text-gray-900 mb-2">Regístrate en Job IT</h2>


                <!-- Divider -->
                <div class="w-full flex items-center justify-center text-gray-500 m-4">¿Deseas registrar tu empresa?
                </div>

                <n-button type="primary" ghost
                    class="w-full flex items-center justify-center border border-gray-300 rounded-md py-2 hover:bg-gray-50 mb-4"
                    block strong @click="handleCompanyRegisterClick" :disabled="isSubmitting">
                    Ir a registro de empresas
                </n-button>

                <!-- Divider -->
                <div class="w-full flex items-center justify-center text-gray-500 m-4">O continúa como&nbsp;<span
                        class="font-bold">candidato</span></div>


                <!-- Form -->

                <n-form ref="formRef" :model="model" :rules="rules">
                    <n-form-item path="firstName" label="Tipo de documento">
                        <n-input v-model:value="model.firstName" placeholder="Cédula de ciudadanía"  />
                    </n-form-item>

                    <n-form-item path="firstName" label="Número de documento">
                        <n-input v-model:value="model.firstName" placeholder="0000000000" />
                    </n-form-item>

                    <n-form-item path="firstName" label="Nombres">
                        <n-input v-model:value="model.firstName" placeholder="Steven" />
                    </n-form-item>

                    <n-form-item path="lastName" label="Apellidos">
                        <n-input v-model:value="model.lastName" placeholder="Job"  />
                    </n-form-item>

                    <n-form-item path="email" label="Correo electrónico">
                        <n-input v-model:value="model.email" placeholder="steven@job.it" />
                    </n-form-item>

                    <n-form-item path="password" label="Contraseña">
                        <n-input v-model:value="model.password" type="password" placeholder="**********" />
                    </n-form-item>

                    <n-form-item path="password" label="Confirma la contraseña">
                        <n-input v-model:value="model.password" type="password" placeholder="**********" />
                    </n-form-item>

                    <!-- Submit -->
                    <n-button type="primary" class="w-full text-white py-2 rounded-md" block strong
                        @click="handleValidateButtonClick" :disabled="isSubmitting">
                        Registrarme
                    </n-button>

                </n-form>



                <!-- Footer -->
                <p class="mt-6 text-center text-sm text-gray-500">
                    ¿Ya tienes una cuenta?
                    <RouterLink to="/account/login" class="text-blue-600 hover:underline ml-1">Inicia sesión
                    </RouterLink>
                </p>

            </div>
        </div>
    </div>

    <div class="hidden md:block bg-now-hiring">
    </div>


</template>
<style scoped>
.bg-now-hiring {
    min-width: 128px;
    min-height: 128px;
    background-image: url('/images/template/job-hiring.svg');
    background-repeat: no-repeat;
    background-position: right center;
    animation: float 3s ease-in-out infinite;
}
</style>