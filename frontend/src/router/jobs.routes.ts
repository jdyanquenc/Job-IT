import { Layout, List, AddEdit } from '@/views/jobs';

export default {
    path: '/jobs',
    component: Layout,
    children: [
        { path: '', component: List },
        { path: 'add', component: AddEdit },
        { path: 'edit/:id', component: AddEdit }
    ]
};
