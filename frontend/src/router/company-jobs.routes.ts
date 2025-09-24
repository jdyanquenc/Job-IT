import { Layout, CompanyJobList, JobAddEdit, JobDetail } from '@/views/jobs'

export default {
  path: '/company-jobs',
  component: Layout,
  children: [
    { path: '', name: 'CompanyJobList', component: CompanyJobList },
    { path: ':id', name: 'CompanyJobDetail', component: JobDetail },
    { path: 'add', name: 'CompanyJobAdd', component: JobAddEdit },
    { path: 'edit/:id', name: 'CompanyJobEdit', component: JobAddEdit },
  ],
}
