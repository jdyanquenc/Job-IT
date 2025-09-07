import { Layout, JobList, JobAddEdit, JobDetail } from '@/views/jobs';

export default {
    path: '/company-jobs',
    component: Layout,
    children: [
        { path: '', name: 'JobList', component: JobList },
        { path: ':id', name: 'JobDetail', component: JobDetail },
        { path: 'add', name: 'JobAdd', component: JobAddEdit },
        { path: 'edit/:id', name: 'JobEdit', component: JobAddEdit },
        
    ]
};

