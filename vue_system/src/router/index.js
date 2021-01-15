import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);



export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/dashboard',
                    component: () => import(/* webpackChunkName: "dashboard" */ '../components/page/Dashboard.vue'),
                    meta: { title: '系统首页', requireAuth: true, roles: ['user', 'admin'] }
                },
                {
                    path: '/icon',
                    component: () => import(/* webpackChunkName: "icon" */ '../components/page/Icon.vue'),
                    meta: { title: '自定义图标', requireAuth: true, roles: ['user', 'admin'] }
                },
                {
                    path: '/table',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/BaseTable.vue'),
                    meta: { title: '我的出题', requireAuth: true, roles: ['user'] }
                },
                {
                    path: '/list',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/BaseList.vue'),
                    meta: { title: '题目列表', requireAuth: true, roles: ['admin'] }
                },
                {
                    path: '/review',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/Review.vue'),
                    meta: { title: '审核题目', requireAuth: true, roles: ['admin'] }
                },
                {
                    path: '/form',
                    component: () => import(/* webpackChunkName: "form" */ '../components/page/BaseForm.vue'),
                    meta: { title: '我要出题', requireAuth: true, roles: ['user', 'admin'] }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403', requireAuth: true, roles: ['user', 'admin'] }
                }
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});

