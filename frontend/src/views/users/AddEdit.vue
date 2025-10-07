<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'

import { NButton, NCard, NCol, NSpin, NForm, NFormItem, NInput, NRow, useMessage } from 'naive-ui'

import { ref } from 'vue'
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useUsersStore } from '@/stores';
import { router } from '@/router';
import type { RegisterUser } from '@/types';


const route = useRoute();
const message = useMessage();
const usersStore = useUsersStore();

const id = route.params.id as string | undefined;

const editMode = ref(false);
const isLoading = ref(false);
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

if (id) {
    isLoading.value = true;
    const { user } = storeToRefs(usersStore);
    usersStore.getById(Number(id))
        .then(() => {
            editMode.value = true;
            model.value.first_name = user.value.first_name;
            model.value.last_name = user.value.last_name;
            model.value.email = user.value.email;
            model.value.password = ''; // Password should not be pre-filled
            isLoading.value = false;

            // User fetched successfully, no additional action needed
        }).catch(() => {
            isLoading.value = false;
            message.error('User not found');
            router.push('/users');
        });
}


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
        required: !editMode.value,
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
        if (editMode.value) {
            // Update existing user
            await usersStore.update(Number(id), registerUser);
            message.success('User updated successfully');
        } else {
            // Register new user
            await usersStore.registerCandidate(registerUser);
            message.success('User registered successfully');
        }
        await router.push('/users');
    }
    catch (error: unknown) {
        console.error('Registration failed:', error);
    }
    finally {
        isSubmitting.value = false;
    }
}


</script>

<template>

    <n-card :title="editMode ? 'Edit User' : 'Add User'" size="large">

        <n-spin :show="isLoading">

            <n-form ref="formRef" :model="model" :rules="rules">
                <n-form-item path="first_name" label="First Name">
                    <n-input v-model:value="model.first_name" @keydown.enter.prevent />
                </n-form-item>

                <n-form-item path="last_name" label="Last Name">
                    <n-input v-model:value="model.last_name" @keydown.enter.prevent />
                </n-form-item>

                <n-form-item path="email" label="Email">
                    <n-input v-model:value="model.email" @keydown.enter.prevent />
                </n-form-item>

                <n-form-item path="password" label="Password">
                    <n-input v-model:value="model.password" type="password" @keydown.enter.prevent />
                </n-form-item>

                <n-form-item path="confirm_password" label="Confirm Password">
                    <n-input v-model:value="model.confirm_password" type="password" @keydown.enter.prevent />
                </n-form-item>

                <n-row :gutter="[0, 24]">
                    <n-col :span="24">
                        <div style="display: flex; justify-content: flex-end">
                            <n-button type="primary" @click="handleValidateButtonClick" :disabled="isSubmitting">
                                {{ editMode ? 'Update' : 'Register' }}
                            </n-button>
                            <router-link to="/users" class="btn btn-link">Cancel</router-link>
                        </div>
                    </n-col>
                </n-row>
            </n-form>

        </n-spin>
    </n-card>

</template>
