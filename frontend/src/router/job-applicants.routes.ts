import { Layout, JobApplicantList } from '@/views/applicants'

export default {
  path: '/jobs',
  component: Layout,
  children: [{ path: ':id/applicants', name: 'JobApplicantList', component: JobApplicantList }],
}
