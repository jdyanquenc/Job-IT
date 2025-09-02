import { Layout, List, AddEdit, JobDetail } from '@/views/jobs';

export default {
    path: '/jobs',
    component: Layout,
    children: [
        { path: '', name: 'JobListing', component: List },
        { path: ':id', name: 'JobDetail', component: JobDetail },
        { path: 'add', component: AddEdit },
        { path: 'edit/:id', component: AddEdit },
        
    ]
};
