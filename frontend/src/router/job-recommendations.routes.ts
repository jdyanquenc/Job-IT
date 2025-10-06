import { Layout, JobRecommendationList } from '@/views/recommendations'

export default {
  path: '/job-recommendations',
  component: Layout,
  children: [{ path: '', name: 'JobRecommendationList', component: JobRecommendationList }],
}
