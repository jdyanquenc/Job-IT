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

const formRef = ref < FormInst | null > (null)

const model = ref < UserCredentials > ({
    username: '',
    password: ''
})

const rules: FormRules = {
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
    <n-card title="Login" class="max-w-screen-sm mx-auto mt-5 mb-5">

        <n-form ref="formRef" :model="model" :rules="rules">
            <n-form-item-row path="username" label="Username">
                <n-input v-model:value="model.username" @keydown.enter.prevent />
            </n-form-item-row>

            <n-form-item-row path="password" label="Password">
                <n-input v-model:value="model.password" type="password" @keydown.enter.prevent />
            </n-form-item-row>
        </n-form>
        <n-button type="primary" block strong
             @click="handleValidateButtonClick"
            :disabled="isSubmitting || (model.username == '' || model.password == '')">
            Login
        </n-button>
    </n-card>
</template>
