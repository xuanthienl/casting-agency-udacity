import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        token: localStorage.getItem('access_token') ? JSON.parse(localStorage.getItem('access_token')).value : null
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
        setJWT({ commit }, data) {
            const now = new Date();
            const token = {
                value: data.access_token,
                expiry: now.getTime() + data.expires_in * 1000
            };
            localStorage.setItem('access_token', JSON.stringify(token));
            commit('setJWT', data.access_token)
        },
        getJWT({ commit }) {
            const accessToken = localStorage.getItem('access_token');
            if (!accessToken) {
                commit('setJWT', null)
            }
            const token = JSON.parse(accessToken);
            const now = new Date().getTime();
            if (now > token.expiry) {
                localStorage.removeItem('access_token');
                commit('setJWT', null)
            }
            return token.value;
        },
        logOut({ commit }) {
            localStorage.removeItem('access_token')
            commit('setJWT', null)
        }
    },
});

export default store;