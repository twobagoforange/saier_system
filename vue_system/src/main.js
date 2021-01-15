import Vue from 'vue';
import App from './App.vue';
import router from './router';
import ElementUI from 'element-ui';
import VueI18n from 'vue-i18n';
import { messages } from './components/common/i18n';
import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import './assets/css/theme-green/index.css'; // 浅绿色主题
import './assets/css/icon.css';
import './components/common/directives';
import 'babel-polyfill';

Vue.config.productionTip = false;
Vue.use(VueI18n);
Vue.use(ElementUI, {
    size: 'small'
});
const i18n = new VueI18n({
    locale: 'zh',
    messages
});

//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | vue-manage-system`;
    const userToken = localStorage.getItem('ms_token');
    const role = localStorage.getItem('ms_role');
    if (role === "user"){

    }
    else if (role === "admin"){

    }
    if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
        console.log('main-token：', userToken);
        if (userToken) { // 判断本地是否存在token
            if (to.meta.roles.length !== 0) {
                for (let i = 0; i < to.meta.roles.length; i++) {
                    if (role === to.meta.roles[i]) {
                        next();
                        break;
                    } else if (i === to.meta.roles.length - 1) {
                        next({
                            path: '/403'
                        });
                    }
                }
            } else {
                next();
            }
        } else {
            next({
                path: '/Login'
            });
        }
    } else {
        next();
    }
    /* 如果本地存在token,则不允许直接跳转到登录页面 */
    if (to.fullPath === '/Login') {
        if (userToken) {
            next({
                path: from.fullPath
            });
        } else {
            next();
        }
    }
});

new Vue({
    router,
    i18n,
    render: h => h(App)
}).$mount('#app');
