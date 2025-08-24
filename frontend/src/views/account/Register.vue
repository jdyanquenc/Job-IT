<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'

import { NButton, NCard, NCol, NForm, NFormItem, NInput, NRow, useMessage } from 'naive-ui'

import { ref } from 'vue'
import { useUsersStore } from '@/stores';
import { router } from '@/router';
import type { RegisterUser } from '@/types';


const message = useMessage();

const isSubmitting = ref(false);

const formRef = ref < FormInst | null > (null)

const model = ref < RegisterUser > ({
    firstName: null,
    lastName: null,
    username: null,
    password: null
})

const rules: FormRules = {
    firstName: {
        required: true,
        message: 'First name is required',
        trigger: 'blur'
    },
    lastName: {
        required: true,
        message: 'Last name is required',
        trigger: 'blur'
    },
    username: {
        required: true,
        message: 'Username is required',
        trigger: 'blur'
    },
    password: {
        required: true,
        message: 'Password is required',
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
                message.error('Please fix the errors before submitting.')
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
    <n-card title="Register" size="large">

        <n-form ref="formRef" :model="model" :rules="rules">
            <n-form-item path="firstName" label="First Name">
                <n-input v-model:value="model.firstName" @keydown.enter.prevent />
            </n-form-item>

            <n-form-item path="lastName" label="Last Name">
                <n-input v-model:value="model.lastName" @keydown.enter.prevent />
            </n-form-item>

            <n-form-item path="username" label="Username">
                <n-input v-model:value="model.username" @keydown.enter.prevent />
            </n-form-item>

            <n-form-item path="password" label="Password">
                <n-input v-model:value="model.password" type="password" @keydown.enter.prevent />
            </n-form-item>

            <n-row :gutter="[0, 24]">
                <n-col :span="24">
                    <div style="display: flex; justify-content: flex-end">
                        <n-button type="primary" @click="handleValidateButtonClick" :disabled="isSubmitting">
                            Register
                        </n-button>
                        <router-link to="login" class="btn btn-link">Cancel</router-link>
                    </div>
                </n-col>
            </n-row>
        </n-form>
    </n-card>
</template>
