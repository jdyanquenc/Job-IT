<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'

import { NButton, NCard, NCol, NForm, NFormItem, NInput, NRow, useMessage } from 'naive-ui'

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
    <n-card title="Login" size="large">

        <n-form ref="formRef" :model="model" :rules="rules">
            <n-form-item path="username" label="Username">
                <n-input v-model:value="model.username" @keydown.enter.prevent />
            </n-form-item>

            <n-form-item path="password" label="Password">
                <n-input v-model:value="model.password" type="password" @keydown.enter.prevent />
            </n-form-item>

            <n-row :gutter="[0, 24]">
                <n-col :span="24">
                    <div style="display: flex; justify-content: flex-end">
                        <n-button type="primary" @click="handleValidateButtonClick"
                            :disabled="isSubmitting || (model.username == '' || model.password == '')">
                            Login
                        </n-button>
                        <router-link to="register" class="btn btn-link">Register</router-link>
                    </div>
                </n-col>
            </n-row>
        </n-form>
    </n-card>
</template>
