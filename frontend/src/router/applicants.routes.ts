import { Layout, ApplicantList } from '@/views/applicants'

export default {
  path: '/jobs',
  component: Layout,
  children: [{ path: ':id/applications', name: 'ApplicantList', component: ApplicantList }],
}
