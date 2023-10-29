import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        token: localStorage.getItem('access_token') || null
    },
    getters: {
        loggedIn(state) {
            return state.token !== null
        }
    },
    mutations: {
        setJWT(state, token) {
            state.token = token
            window.location.href = '/';
        }
    },
    actions: {
        login() {
            window.location.href = 'https://' + process.env.VUE_APP_AUTH0_DOMAIN +
                '/authorize?audience=' + process.env.VUE_APP_AUTH0_API_AUDIENCE +
                '&response_type=' + process.env.VUE_APP_AUTH0_RESPONSE_TYPE +
                '&client_id=' + process.env.VUE_APP_AUTH0_CLIENT_ID +
                '&redirect_uri=' + process.env.VUE_APP_AUTH0_CALLBACK_URL
        },
        logout({ commit }) {
            localStorage.removeItem('access_token')
            commit('setJWT', null)
        },
        setJWT({ commit }, hash) {
            const fragment = hash.substr(1).split('&')[0].split('=');
            if (fragment[0] === 'access_token') {
                const token = fragment[1];
                localStorage.setItem('access_token', token)
                commit('setJWT', token)
            }
        }
    },
});

export default store;