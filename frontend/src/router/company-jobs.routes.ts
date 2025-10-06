import { Layout, CompanyJobList, CompanyJobAddEdit } from '@/views/company-jobs'
import { JobDetail } from '@/views/jobs'

export default {
  path: '/company-jobs',
  component: Layout,
  children: [
    { path: '', name: 'CompanyJobList', component: CompanyJobList },
    { path: 'add', name: 'CompanyJobAdd', component: CompanyJobAddEdit },
    { path: 'edit/:id', name: 'CompanyJobEdit', component: CompanyJobAddEdit },
    { path: ':id', name: 'CompanyJobDetail', component: JobDetail },
  ],
}
