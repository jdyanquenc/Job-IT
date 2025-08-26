<script setup lang="ts">

import { h } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia';
import { useUsersStore } from '@/stores';

import { NDataTable, NButton, useMessage } from 'naive-ui'

import SearchBar from '@/views/jobs/SearchBar.vue'
import type { User } from '@/types/User';

const message = useMessage();
const usersStore = useUsersStore();
const router = useRouter()
const { users } = storeToRefs(usersStore);

usersStore.getAll();

const pagination = false;

// Button actions
const handleEdit = (row: User) => {
    router.push(`/users/edit/${row.id}`)
}


const handleDelete = (row: User) => {
    // Confirm before deleting
    usersStore.delete(row.id)
        .then(() => {
            message.success('User deleted successfully');
        })
        .catch((error) => {
            console.error('Error deleting user:', error);
            message.error('Failed to delete user');
        });
}


const columns = [
    {
        title: 'ID',
        key: 'id'
    },
    {
        title: 'First Name',
        key: 'firstName',
    },
    {
        title: 'Last Name',
        key: 'lastName',
    },
    {
        title: 'Username',
        key: 'username',
    },
    {
        title: 'Action',
        key: 'actions',
        render(row: User) {
            return h('div', { class: 'flex gap-2' }, [
                h(
                    NButton,
                    {
                        size: 'small',
                        type: 'primary',
                        onClick: () => handleEdit(row)
                    },
                    { default: () => 'Edit' }
                ),
                h(
                    NButton,
                    {
                        size: 'small',
                        type: 'error',
                        onClick: () => handleDelete(row)
                    },
                    { default: () => 'Delete' }
                )
            ])
        }
    }
]

</script>

<template>

<div class="grid grid-cols-1 md:grid-cols-12 gap-4 min-h-screen">

    <div class="md:col-span-12 pt-3">
        <h1>Users</h1>
        <SearchBar />
        <router-link to="/users/add" class="btn btn-sm btn-success mb-2">Add User</router-link>
        <n-data-table :columns="columns" :data="users" :pagination="pagination" :bordered="false" />
    </div>

</div>



    


    

    <!-- 
    <table class="table table-striped">
        <thead>
            <tr>
                <th style="width: 30%">First Name</th>
                <th style="width: 30%">Last Name</th>
                <th style="width: 30%">Username</th>
                <th style="width: 10%"></th>
            </tr>
        </thead>
        <tbody>
            <template v-if="users.length">
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.firstName }}</td>
                    <td>{{ user.lastName }}</td>
                    <td>{{ user.username }}</td>
                    <td style="white-space: nowrap">
                        <router-link :to="`/users/edit/${user.id}`"
                            class="btn btn-sm btn-primary mr-1">Edit</router-link>
                        <button @click="usersStore.delete(user.id)" class="btn btn-sm btn-danger btn-delete-user"
                            :disabled="user.isDeleting">
                            <span v-if="user.isDeleting" class="spinner-border spinner-border-sm"></span>
                            <span v-else>Delete</span>
                        </button>
                    </td>
                </tr>
            </template>
<tr v-if="users.loading">
    <td colspan="4" class="text-center">
        <span class="spinner-border spinner-border-lg align-center"></span>
    </td>
</tr>
<tr v-if="users.error">
    <td colspan="4">
        <div class="text-danger">Error loading users: {{ users.error }}</div>
    </td>
</tr>
</tbody>
</table> -->
</template>
