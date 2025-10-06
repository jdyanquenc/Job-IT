import { Layout, JobApplicationList } from '@/views/applications'

export default {
  path: '/job-applications',
  component: Layout,
  children: [{ path: '', name: 'JobApplicationList', component: JobApplicationList }],
}
