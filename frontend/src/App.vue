<template>
    <div class="container vh-100" id="app">
        <UserLogin v-if="!this.$store.getters.loggedIn"/>
        <AppHeader v-if="this.$store.getters.loggedIn"/>
        <router-view v-if="this.$store.getters.loggedIn"></router-view>
        <notifications class="notifications" group="foo"/>
    </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import UserLogin from './components/UserLogin.vue'

export default {
    name: 'App',
    components: {
        AppHeader,
        UserLogin
    }
}
</script>
