<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'

import { NButton, NForm, NFormItem, NInput, NSelect, c, useMessage } from 'naive-ui'

import { ref } from 'vue'
import { useUsersStore } from '@/stores';
import { router } from '@/router';
import type { RegisterUser } from '@/types';


const message = useMessage();

const isSubmitting = ref(false);
const formRef = ref<FormInst | null>(null)

const model = ref<RegisterUser>({
    identification_type: null,
    identification_number: null,
    first_name: null,
    last_name: null,
    email: null,
    password: null,
    confirm_password: null
})

const rules: FormRules = {
    identification_type: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    identification_number: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    first_name: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    last_name: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    email: {
        validator: async (rule, value) => {
            if (!value) {
                return Promise.reject('Este campo es requerido')
            }
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            if (!emailRegex.test(value)) {
                return Promise.reject('Correo no válido')
            }

            const exists = await checkEmailAvailability(value)
            if (exists) {
                return Promise.reject('Este correo ya está registrado')
            }

            return Promise.resolve() // Change here to return void
        },
        trigger: 'blur'
    },
    password: {
        validator: (rule, value) => {
            if (!value) {
                return Promise.reject('Este campo es requerido')
            }
            if (value.length < 8) {
                return Promise.reject('La contraseña debe tener al menos 8 caracteres')
            }
            if (!/[A-Z]/.test(value)) {
                return Promise.reject('La contraseña debe contener al menos una letra mayúscula')
            }
            if (!/[a-z]/.test(value)) {
                return Promise.reject('La contraseña debe contener al menos una letra minúscula')
            }
            if (!/[0-9]/.test(value)) {
                return Promise.reject('La contraseña debe contener al menos un número')
            }
            if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
                return Promise.reject('La contraseña debe contener al menos un carácter especial')
            }
            if (model.value.confirm_password && value !== model.value.confirm_password) {
                return Promise.reject('Las contraseñas no coinciden')
            }
            return Promise.resolve()
        },
        trigger: ['blur', 'input']
    },
    confirm_password: {
        validator: async (rule, value) => {
            if (value !== model.value.password) {
                return Promise.reject('Las contraseñas no coinciden')
            }
            return Promise.resolve()
        },
        trigger: ['blur', 'input']
    }
};

const identification_types = [
    { label: 'Cédula de ciudadanía', value: 'CC' },
    { label: 'Cédula de extranjería', value: 'CE' },
    { label: 'Pasaporte', value: 'PA' },
    { label: 'Tarjeta de identidad', value: 'TI' }
]


function handleCompanyRegisterClick() {
    router.push('/accounts/register-company');
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

async function checkEmailAvailability(email: string): Promise<boolean> {
    const usersStore: ReturnType<typeof useUsersStore> = useUsersStore();
    const validationResult = await usersStore.checkEmailAvailability(email);
    return Promise.resolve(!validationResult.available);
}


async function onSubmit() {
    const usersStore: ReturnType<typeof useUsersStore> = useUsersStore();
    const registerUser: RegisterUser = model.value;

    try {
        isSubmitting.value = true;
        await usersStore.registerCandidate(registerUser);
        await router.push('/accounts/login');
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
                    <n-form-item path="identification_type" label="Tipo de documento">
                        <n-select v-model:value="model.identification_type" :options="identification_types"
                            placeholder="Selecciona una opción" />
                    </n-form-item>

                    <n-form-item path="identification_number" label="Número de documento">
                        <n-input v-model:value="model.identification_number" placeholder="0000000000" />
                    </n-form-item>

                    <n-form-item path="first_name" label="Nombres">
                        <n-input v-model:value="model.first_name" placeholder="Steve" />
                    </n-form-item>

                    <n-form-item path="last_name" label="Apellidos">
                        <n-input v-model:value="model.last_name" placeholder="Jobs" />
                    </n-form-item>

                    <n-form-item path="email" label="Correo electrónico">
                        <n-input v-model:value="model.email" placeholder="steve@jobs.it" />
                    </n-form-item>

                    <n-form-item path="password" label="Contraseña">
                        <n-input v-model:value="model.password" type="password" placeholder="**********" />
                    </n-form-item>

                    <n-form-item path="confirmPassword" label="Confirma la contraseña">
                        <n-input v-model:value="model.confirm_password" type="password" placeholder="**********" />
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
                    <RouterLink to="/accounts/login" class="text-blue-600 hover:underline ml-1">Inicia sesión
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