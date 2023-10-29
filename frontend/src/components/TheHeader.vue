<template>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container-fluid">
            <a class="navbar-brand text-custom" href="/">Casting Agency</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'movies' }"
                            v-bind:class="[$route.name == 'movies' ? 'active' : '']">Movies</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'actors' }"
                            v-bind:class="[$route.name == 'actors' ? 'active' : '']">Actors</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'casting' }"
                            v-bind:class="[$route.name == 'casting' ? 'active' : '']">Casting</router-link>
                    </li>
                </ul>
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="user" data-bs-toggle="dropdown" aria-expanded="false">
                        <font-awesome-icon icon="house-chimney-user"/>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="user">
                        <button type="button" v-if="!this.$store.getters.loggedIn" v-on:click="Login()">
                            <font-awesome-icon icon="fa-solid fa-circle-chevron-up" />
                            Login
                        </button>
                        <button type="button" v-if="this.$store.getters.loggedIn" v-on:click="Logout()">
                            <font-awesome-icon icon="fa-solid fa-circle-chevron-down" />
                            Logout
                        </button>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    // mounted() {
    //     if (!this.$store.getters.loggedIn) {
    //         this.Login()
    //     }
    // },
    methods: {
        Login() {
            this.$store.dispatch('login')
        },
        Logout() {
            this.$store.dispatch('logout')
        }
    }
}
</script>
