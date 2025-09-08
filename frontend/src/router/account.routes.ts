import { Layout, Login, Register, RegisterCompany } from '@/views/account';

export default {
    path: '/account',
    component: Layout,
    children: [
        { path: '', redirect: 'login' },
        { path: 'login', component: Login },
        { path: 'register', component: Register },
        { path: 'register-company', component: RegisterCompany }
    ]
};
