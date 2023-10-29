import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import Home from './views/TheHome.vue';
import Movie from './views/TheMovie.vue';
import Actor from './views/TheActor.vue';
import Casting from './views/TheCasting.vue';
import Login from './views/TheLogin.vue';

const routes = [
    { path: '/', name: 'home', component: Home },
    { path: '/movies', name: 'movies', component: Movie },
    { path: '/actors', name: 'actors', component: Actor },
    { path: '/casting', name: 'casting', component: Casting },
    { path: '/login-results', name: 'login', component: Login },
    { path: '/:pathMatch(.*)*', redirect: { name: 'home' } }
];

const router = new VueRouter({
    mode:'history',
    routes
});

router.beforeEach((to, from, next) => {
    let title = to.meta.title || 'Casting Agency Group';
    document.title = title;
    next();
});

export default router;