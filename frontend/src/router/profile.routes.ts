import { Layout, UserProfileEdit, UserProfileDetail } from '@/views/profile'

export default {
  path: '/profile',
  component: Layout,
  children: [
    { path: ':id', name: 'UserProfileDetail', component: UserProfileDetail },
    { path: 'edit/:id', name: 'UserProfileEdit', component: UserProfileEdit },
  ],
}
