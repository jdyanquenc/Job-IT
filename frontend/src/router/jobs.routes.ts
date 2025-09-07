import { Layout, JobList, JobAddEdit, JobDetail } from '@/views/jobs';

export default {
    path: '/jobs',
    component: Layout,
    children: [
        { path: '', name: 'JobList', component: JobList },
        { path: ':id', name: 'JobDetail', component: JobDetail }
    ]
};

